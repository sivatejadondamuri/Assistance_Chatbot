import os
import time
import tempfile
import threading
from flask import Flask, request, jsonify, render_template
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader, UnstructuredWordDocumentLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from google import genai
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# --- Configuration & Initialization ---
app = Flask(__name__)

# The execution environment provides the key at runtime via an empty string.
api_key = ""
client = genai.Client(api_key=api_key)

# Initialize Embedding Model (Objective: all-MiniLM-L6-v2)
print("Loading Embedding Model (all-MiniLM-L6-v2)...")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Thread-safe Global Store for Vector Index and Chunks
class DocState:
    def __init__(self):
        self.index = None
        self.chunks = []
        self.lock = threading.Lock()

state = DocState()

# --- Core Logic & Utility Functions ---

def call_gemini(prompt):
    """Utility to call Gemini 2.5 Flash with exponential backoff retry logic."""
    retries = 5
    for i in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-preview-09-2025",
                contents=prompt
            )
            return response.text
        except Exception:
            if i == retries - 1:
                raise
            # Backoff: 1s, 2s, 4s, 8s, 16s
            time.sleep(2**i)
    return ""

def process_and_index_pipeline(raw_text, source_name):
    """
    INTERNAL PIPELINE:
    1. Summarize and organize using Gemini (Objective Prompt 1).
    2. Chunk the summary (Size 500, Overlap 50).
    3. Embed and store in internal FAISS index.
    """
    if not raw_text or len(raw_text.strip()) < 20:
        raise Exception("Retrieved content is too short to process.")

    # Step 1: High-level Summarization (Internal Objective)
    # Translation instruction ensures RAG context is always in English for better retrieval accuracy
    summary_prompt = f"""Here are the contents of a source ({source_name}):
    {raw_text[:15000]}
    
    Summarize and organize the data in an order. If the extracted text language is not English, translate the text into English. 
    Ensure the output is in English so that it should be easy to understand the contents of this website and can be easily understand the routes/sections."""
    
    summarized_content = call_gemini(summary_prompt)
    if not summarized_content:
        raise Exception("AI Summarization failed.")

    # Step 2: Chunking the generated summary
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents([Document(page_content=summarized_content)])
    
    # Step 3: Create Embeddings and store in Index
    texts = [c.page_content for c in chunks]
    embeddings = embed_model.encode(texts)
    
    with state.lock:
        dimension = embeddings.shape[1]
        if state.index is None:
            state.index = faiss.IndexFlatL2(dimension)
        
        # FAISS requires float32 numpy arrays
        state.index.add(np.array(embeddings).astype('float32'))
        state.chunks.extend(texts)
    
    return len(chunks)

# --- Flask Routes ---

@app.route('/')
def home():
    """Renders the main dashboard."""
    return render_template('index.html')

@app.route('/upload_url', methods=['POST'])
def upload_url():
    """Scrapes URL, Summarizes, and Indexes."""
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    try:
        # Browser-like headers to prevent scraping blocks/403 errors
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        loader = WebBaseLoader(web_path=url, header_template=headers)
        docs = loader.load()
        
        if not docs:
            return jsonify({"error": "Failed to extract content from URL."}), 400
            
        chunk_count = process_and_index_pipeline(docs[0].page_content, url)
        return jsonify({"message": "URL summarized and indexed successfully.", "count": chunk_count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload_file', methods=['POST'])
def upload_file():
    """Loads PDF/Docs, Extracts text, Summarizes, and Indexes."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    suffix = os.path.splitext(file.filename)[1].lower()
    
    try:
        # Use a secure temp file handling method
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name

        try:
            # Text extraction based on file format
            if suffix == '.pdf':
                loader = PyPDFLoader(tmp_path)
            elif suffix in ['.doc', '.docx']:
                loader = UnstructuredWordDocumentLoader(tmp_path)
            else:
                loader = TextLoader(tmp_path)
                
            docs = loader.load()
            
            if not docs:
                return jsonify({"error": "No text could be extracted from this file."}), 400

            full_text = "\n".join([d.page_content for d in docs])
            chunk_count = process_and_index_pipeline(full_text, file.filename)
            return jsonify({"message": f"'{file.filename}' summarized and indexed.", "count": chunk_count})
        
        finally:
            # Always clean up the temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
                
    except Exception as e:
        return jsonify({"error": f"File processing error: {str(e)}"}), 500

@app.route('/get_greeting', methods=['POST'])
def get_greeting():
    """Requirement: Bot asks 'How can I help you?' in the target language."""
    lang = request.json.get('language', 'English')
    prompt = f"Give the text - 'How can I help you?' in {lang} language. Return ONLY the translated text."
    greeting = call_gemini(prompt)
    return jsonify({"greeting": greeting.strip()})

@app.route('/chat', methods=['POST'])
def chat():
    """RAG flow: Query Embedding -> Top-2 Retrieve -> Multilingual Detailed Answer."""
    data = request.json
    query = data.get('message')
    lang = data.get('language', 'English')

    if state.index is None or len(state.chunks) == 0:
        return jsonify({"answer": "I have no data. Please provide a URL or File first."})

    # Step 0: Translate the query to English before embedding to match the English index
    translation_prompt = f"Translate the following user query to English. If it is already in English, return it exactly as is: {query}"
    english_query = call_gemini(translation_prompt).strip()

    # Step 1: Embed English Query and Search (Top 2 retrieval)
    query_embedding = embed_model.encode([english_query])
    distances, indices = state.index.search(np.array(query_embedding).astype('float32'), k=2)
    
    retrieved_docs = [state.chunks[i] for i in indices[0] if i < len(state.chunks)]
    context = "\n".join(retrieved_docs)

    # Step 2: Detailed Multilingual Response generation (Objective Prompt 2)
    final_prompt = f"""
    Use the following context to answer the question.
    Context:
    {context}
    
    User Question: {query}
    
    Target Language: {lang}
    
    Explain the answer in detail. The final response MUST be in {lang}.
    """
    
    answer = call_gemini(final_prompt)
    return jsonify({"answer": answer})

@app.route('/clear', methods=['POST'])
def clear_session():
    """Clears the internal state."""
    with state.lock:
        state.index = None
        state.chunks = []
    return jsonify({"status": "cleared"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
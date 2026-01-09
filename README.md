# Multilingual DocChat: Hyper-Local RAG for Linguistic Diversity 🌍📄

A **production-ready Retrieval-Augmented Generation (RAG) system** designed to bridge the linguistic divide.  
This project implements a **Cross-lingual RAG (CrossRAG)** approach, enabling users to interact with complex documents and web content in **22+ Indian languages**.

---

## 📌 Problem Statement

In linguistically diverse regions like **India**, language becomes a major barrier to digital sovereignty.

While **Large Language Models (LLMs)** perform exceptionally well in **English**, their ability to reason deeply and retrieve accurate information drops significantly for **low-resource regional languages**.

### ❌ Limitations of Standard RAG Systems

- **Linguistic Performance Gaps**  
  LLMs reason better in English than in regional dialects.

- **Information Extraction Challenges**  
  Legal, agricultural, and government data are often stored in localized formats that global models fail to index effectively.

- **The Digital Divide**  
  Non-English speaking users (e.g., farmers, local administrators, legal clerks) lack tools to query data in their native language.

---

## 🚀 Our Solution: Cross-lingual RAG (CrossRAG)

This project introduces a **language-bridged RAG architecture**.

Instead of forcing the LLM to reason entirely in a low-resource language, **English is used internally as a bridge language**, while the **user interacts fully in their native language**.

---

## 🔁 CrossRAG Pipeline Logic

### 1️⃣ Ingestion  
- Scrapes web URLs  
- Parses PDF and DOCX files  

### 2️⃣ Summarization & Translation  
- **Gemini 2.5 Flash** summarizes and translates content into English  
- Ensures high-quality semantic indexing  

### 3️⃣ Semantic Indexing  
- English summaries are chunked  
- Stored in a **FAISS vector database**  
- Embedded using **all-MiniLM-L6-v2**

### 4️⃣ Query Translation  
- User queries (Telugu, Hindi, etc.) are translated into English  
- Enables accurate semantic search  

### 5️⃣ Multilingual Answer Synthesis  
- Relevant English context is retrieved  
- Final response is generated **in the user’s selected language**

---

## 🛠️ Technologies Used

### 🔧 Backend
- **Python**
- **Flask**

### 🧠 LLM Interface
- **Google Gemini 2.5 Flash** (`google-genai`)

### 🔗 Orchestration
- **LangChain**

### 📦 Vector Database
- **FAISS** (Facebook AI Similarity Search)

### 🧬 Embeddings
- **Sentence-Transformers**
- Model: `all-MiniLM-L6-v2`

### 📂 Document Loaders
- `WebBaseLoader`
- `PyPDFLoader`
- `UnstructuredWordDocumentLoader`

### 🎨 Frontend
- **HTML5**
- **Tailwind CSS**
- **FontAwesome**

---

## 📁 Project Structure

```text
multilingual-docchat/
│
├── app.py                 # Flask server with CrossRAG pipeline
├── requirements.txt       # Python dependencies
│
├── templates/
│   └── index.html         # Multilingual chat dashboard
│
└── README.md              # Project documentation

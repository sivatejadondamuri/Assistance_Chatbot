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

```
multilingual-docchat/
│
├── app.py                 # Flask server with CrossRAG pipeline
├── requirements.txt       # Python dependencies
│
├── templates/
│   └── index.html         # Multilingual chat dashboard
│
└── README.md              # Project documentation

```
## 🚥 Getting Started
### ✅ Prerequisites

Python 3.9+


Google Gemini API Key



## 📥 Installation
### 1️⃣ Clone the Repository
- git clone https://github.com/your-username/multilingual-docchat.git
- cd multilingual-docchat

### 2️⃣ Install Dependencies
- pip install -r requirements.txt

### 3️⃣ Configure API Key
- Edit app.py and add your Gemini API key:
- api_key = "YOUR_GEMINI_API_KEY"

### 4️⃣ Run the Application
- python app.py

- Open your browser and navigate to:
- http://127.0.0.1:5000


## 🌐 Supported Languages


- Telugu


- Hindi


- Tamil


- Kannada


- Malayalam


- Marathi


- Bengali


- Gujarati


- Punjabi


- Odia


- Urdu


- Assamese


- and more (22+ total)



## ⚖️ Case Study Inspiration
This system is inspired by hyper-local agricultural and governance needs in regions like Andhra Pradesh.
Example Use Case:


- Processing state agricultural portals


- Indexing Agmarknet datasets


- Allowing farmers to query:


- Crop pricing


- Compliance rules


- Government schemes




- All in Telugu

This approach significantly outperforms English-only search systems and makes AI accessible, inclusive, and practical.

### 🌟 Key Advantages


- ✅ High retrieval accuracy using English embeddings


- ✅ Native-language interaction for users


- ✅ Works for low-resource languages


- ✅ Scalable and production-ready


- ✅ Ideal for legal, agricultural, and government data



## 📜 License
This project is open-source and available under the MIT License.

🤝 Contributions
Contributions are welcome!
Feel free to open issues or submit pull requests to improve multilingual coverage, UI, or performance.

Empowering local languages with global AI intelligence. 🌏✨

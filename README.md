# 📄 RAG SOP Assistant — Chat with PDF

An AI-powered PDF Question Answering system built using 
RAG (Retrieval-Augmented Generation) architecture.
Upload any PDF and ask questions — get precise answers 
directly from the document.

---

## ✨ Features

- 📂 Upload **any PDF** document
- 💬 Ask questions in **natural language**
- ✅ Get **precise answers** from the document
- ⚠️ Shows **"Not found in document"** for irrelevant questions
- 🔄 **Chat history** — see all previous Q&A
- 🗑️ Clear chat anytime
- 🤖 Works **without internet** — fully local

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Vector Store | FAISS |
| PDF Loader | LangChain PyPDFLoader |
| UI | Streamlit |
| API | FastAPI |
| Language | Python 3.11 |

---

## 📁 Project Structure
rag_sop_assistant/
├── src/
│   ├── query.py          # Core RAG logic
│   ├── ingest.py         # PDF ingestion
│   ├── streamlit_app.py  # Chat UI
│   └── api.py            # FastAPI endpoints
├── data/
│   └── policy.pdf        # Sample PDF
├── vectorstore/
│   └── faiss_index/      # FAISS index files
├── .env
├── requirements.txt
└── README.md

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/snehagondinigari24-lab/rag-sop-assistent.git
cd rag-sop-assistent

2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

3. Install dependencies
pip install -r requirements.txt

▶️ Run the App
streamlit run src/streamlit_app.py
Open browser: http://localhost:8501

🚀 How to Use
Open the app in browser
Upload any PDF from the sidebar
Click "Process PDF"
Type your question and click "Search"
Get answer from the document!

📊 How It Works
User uploads PDF
      ↓
PDF split into chunks
      ↓
Chunks converted to embeddings (HuggingFace)
      ↓
Stored in FAISS vector store
      ↓
User asks question
      ↓
FAISS finds most similar chunks
      ↓
Answer extracted from best chunk
      ↓
Displayed in chat UI

📦 Requirements
langchain
langchain-community
faiss-cpu
sentence-transformers
streamlit
fastapi
uvicorn
pypdf
python-dotenv

👩‍💻 Author
Sneha Gondinigari
GitHub: @snehagondinigari24-lab

## 🎥 Demo Video
[▶️ Click here to watch Demo](https://github.com/snehagondinigari24-lab/rag-sop-assistent/blob/main/rag_sop_assistent.mp4)


📄 License
MIT License

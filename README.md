# Multimodal RAG Chatbot  
**Django + Gemini 1.5 + FAISS + HuggingFace**  

A **PDF-powered RAG chatbot** that understands **text, tables, graphs, and images** using **Google Gemini Vision** and **vector search**.

---

## Features
- Upload **PDFs** (with tables, charts, images)
- Extract **text**, **tables**, and **images**
- Embed with **HuggingFace** (`all-MiniLM-L6-v2`)
- Store in **FAISS** vector database
- Answer questions using **Gemini 1.5 Flash (multimodal)**
- Return **answer + source pages/types**
- CLI & API ready

---

## Tech Stack
| Component | Technology |
|--------|------------|
| Backend | Django REST Framework |
| PDF Processing | PyMuPDF + pdfplumber |
| Embeddings | `sentence-transformers` |
| Vector DB | FAISS |
| LLM | Google Gemini 1.5 Flash |
| API | `/api/upload/`, `/api/chat/` |

---

## Project Structure

rag_chatbot_django/
├── rag_app/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── utils/
│       ├── pdf_processor.py
│       ├── vector_store.py
│       └── rag_bot.py
├── media/
│   └── processed/     ← FAISS + images per doc
├── .env
├── .gitignore
├── requirements.txt
├── manage.py
└── README.md


---

## Setup

### 1. Clone & Enter
```bash
git clone https://github.com/yourusername/rag-chatbot-django.git
cd rag-chatbot-django

python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate  # macOS/Linux

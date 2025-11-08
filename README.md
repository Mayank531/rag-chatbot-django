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

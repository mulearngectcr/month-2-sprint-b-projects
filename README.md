# AI Documentation Assistant

A minimal RAG-based AI Documentation Assistant to upload PDFs and ask questions grounded strictly in the uploaded documents, returning answers with source citations, page numbers, and similarity scores.

Built for free cloud hosting using FastAPI, ChromaDB (with ONNX embedding function, zero PyTorch/sentence-transformers), Groq (llama-3.3-70b-versatile), and Streamlit.

## Environment Variables

Copy `.env.example` to `.env` and set your Groq API key:
```text
GROQ_API_KEY=your_groq_api_key_here
```

## Local Development

1. Create and activate a Python virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install pinned dependencies:
```powershell
pip install -r requirements.txt
```

3. Run the FastAPI backend:
```powershell
uvicorn app:app --reload
```
API documentation is available at `http://localhost:8000/docs`.

4. Run the Streamlit frontend (in a separate terminal):
```powershell
streamlit run frontend.py
```

## Live Demo

- **Frontend (Streamlit Cloud):** `https://month-2-sprint-b-projects-pznejltfnnwquw5dqyzq8w.streamlit.app`
- **Backend (Render):** `https://month-2-sprint-b-projects-hnjr.onrender.com/docs`

## Deployment Guide

### Backend: Render (Free Web Service)
- **Repository:** your forked repo
- **Branch:** `athul-pp`
- **Root Directory:** *(leave blank)*
- **Runtime:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
- **Health Check Path:** `/health`
- **Environment Variables:** `GROQ_API_KEY` = your Groq API key
- *Note:* The service URL has a random suffix; copy the exact URL from your Render dashboard.

### Frontend: Streamlit Community Cloud
- **Repository:** your forked repo
- **Branch:** `athul-pp`
- **Main file path:** `frontend.py`
- **App settings / Secrets:**
```toml
BACKEND_URL = "<exact Render URL, no trailing slash>"
```

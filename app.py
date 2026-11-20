from fastapi import FastAPI, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import rag

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str
    top_k: int = 4

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    results = {}
    for f in files:
        results[f.filename] = rag.ingest(f.file, f.filename)
    return results

@app.post("/ask")
async def ask(req: AskRequest):
    ans, sources = rag.answer(req.question, req.top_k)
    return {"answer": ans, "sources": sources}

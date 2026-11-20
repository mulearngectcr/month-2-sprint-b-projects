import os
from pypdf import PdfReader
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = chromadb.PersistentClient(path="./chroma_db")
ef = DefaultEmbeddingFunction()
collection = client.get_or_create_collection(
    name="docs",
    embedding_function=ef,
    metadata={"hnsw:space": "cosine"},
)

def ingest(file_obj, filename: str) -> int:
    try:
        collection.delete(where={"source": filename})
    except Exception:
        pass
    reader = PdfReader(file_obj)
    docs, metas, ids = [], [], []
    chunk_count = 0
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = text.strip()
        if not text:
            continue
        start = 0
        while start < len(text):
            chunk = text[start : start + 500]
            docs.append(chunk)
            metas.append({"source": filename, "page": page_num, "chunk_index": chunk_count})
            ids.append(f"{filename}-{chunk_count}")
            chunk_count += 1
            if start + 500 >= len(text):
                break
            start += 450
    if docs:
        collection.add(ids=ids, documents=docs, metadatas=metas)
    return chunk_count

def retrieve(question: str, top_k: int = 4):
    count = collection.count()
    if count == 0:
        return []
    res = collection.query(query_texts=[question], n_results=min(top_k, count))
    results = []
    if res and res["documents"] and res["documents"][0]:
        for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
            results.append({
                "source": meta["source"],
                "page": meta["page"],
                "chunk_index": meta["chunk_index"],
                "score": round(1.0 - dist, 4),
                "text": doc,
            })
    return results

def answer(question: str, top_k: int = 4):
    sources = retrieve(question, top_k)
    if not sources:
        return "No documents found. Please upload a PDF first.", []
    context = "\n\n".join(s["text"] for s in sources)
    prompt = f"Answer only using the context below. If the answer isn't there, say you don't know.\n\nContext:\n{context}\n\nQuestion: {question}"
    client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
    resp = client_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content, sources

import os
import streamlit as st
import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

st.set_page_config(page_title="AI Documentation Assistant")
st.title("AI Documentation Assistant")

with st.sidebar:
    st.header("Upload PDFs")
    uploaded = st.file_uploader("Choose PDFs", type=["pdf"], accept_multiple_files=True)
    if st.button("Ingest") and uploaded:
        files = [("files", (f.name, f.getvalue(), "application/pdf")) for f in uploaded]
        with st.spinner("Ingesting PDFs... (may take up to 2 min if waking up)"):
            try:
                res = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=120)
                if res.status_code == 200:
                    st.success("Ingested successfully!")
                    st.json(res.json())
                else:
                    st.error(f"Error {res.status_code}: {res.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")

question = st.text_input("Ask a question:")
top_k = st.number_input("Top K sources:", min_value=1, max_value=10, value=4)

if st.button("Ask") and question:
    with st.spinner("Generating answer... (may take up to 2 min if waking up)"):
        try:
            res = requests.post(
                f"{BACKEND_URL}/ask",
                json={"question": question, "top_k": int(top_k)},
                timeout=120,
            )
            if res.status_code == 200:
                data = res.json()
                st.subheader("Answer")
                st.write(data.get("answer", ""))
                st.subheader("Sources")
                for s in data.get("sources", []):
                    st.markdown(
                        f"**{s.get('source')}** | Page {s.get('page')} | Score: {s.get('score')}"
                    )
                    st.text(s.get("text", ""))
            else:
                st.error(f"Error {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")

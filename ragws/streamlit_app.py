from pathlib import Path

import requests
import streamlit as st

from bmw_rag.settings import settings

st.set_page_config(
    page_title="BMW RAG Assistant",
    page_icon="🚘",
)

st.title("🚘 BMW Document RAG Assistant")

uploads = st.file_uploader(
    "Upload PDF or DOCX documents",
    type=["pdf", "docx"],
    accept_multiple_files=True,
)

if st.button("Save and Index Documents"):
    for upload in uploads:
        file_path = settings.document_directory / Path(upload.name).name
        settings.document_directory.mkdir(
            parents=True,
            exist_ok=True,
        )
        file_path.write_bytes(upload.getvalue())

    response = requests.post(
        f"{settings.api_base_url}/ingest",
        timeout=300,
    )

    st.success(response.json()["message"])

question = st.text_input(
    "Ask a question about your documents"
)

if st.button("Ask Question") and question:
    response = requests.post(
        f"{settings.api_base_url}/ask",
        json={"question": question},
        timeout=300,
    )

    result = response.json()

    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Sources")
    for source in result["sources"]:
        st.write(
            f"- {source['file']} "
            f"(Page: {source['page'] or 'N/A'})"
        )
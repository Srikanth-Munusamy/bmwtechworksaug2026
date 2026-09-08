from pathlib import Path

import requests
import streamlit as st

from bmw_rag.settings import settings

# -------------------------------------------------
# Streamlit configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Multi Tenant RAG Assistant",
    page_icon="🚘",
)

st.title("🚘 Multi-Tenant Document RAG Assistant")

# -------------------------------------------------
# Select client
# -------------------------------------------------

client = st.selectbox(
    "Client",
    [
        "toyota",
        "bmw",
    ],
)

# -------------------------------------------------
# Upload documents
# -------------------------------------------------

uploads = st.file_uploader(
    "Upload PDF or DOCX documents",
    type=["pdf", "docx"],
    accept_multiple_files=True,
)

# -------------------------------------------------
# Save and index documents
# -------------------------------------------------

if st.button("Save and Index Documents"):
    if not uploads:
        st.warning(
            "Please upload at least one PDF or DOCX file."
        )
    else:
        # Creates:
        # bmw/documents/
        # toyota/documents/
        client_document_directory = (
            Path(client)
            / Path(settings.document_directory).name
        )

        client_document_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        saved_files = []

        for upload in uploads:
            safe_file_name = Path(upload.name).name

            file_path = (
                client_document_directory
                / safe_file_name
            )

            file_path.write_bytes(
                upload.getvalue()
            )

            saved_files.append(
                safe_file_name
            )

        try:
            response = requests.post(
                f"{settings.api_base_url}/ingest",
                params={
                    "client": client,
                },
                timeout=300,
            )

            response.raise_for_status()

            result = response.json()

            st.success(
                result.get(
                    "message",
                    "Documents indexed successfully.",
                )
            )

            st.write(
                f"Saved {len(saved_files)} file(s) "
                f"for {client.upper()}."
            )

        except requests.RequestException as error:
            st.error(
                f"Indexing failed: {error}"
            )

# -------------------------------------------------
# Ask question
# -------------------------------------------------

st.divider()

question = st.text_input(
    f"Ask a question about {client.upper()} documents"
)

if st.button("Ask Question"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            response = requests.post(
                f"{settings.api_base_url}/ask",
                json={
                    "client": client,
                    "question": question,
                },
                timeout=300,
            )

            response.raise_for_status()

            result = response.json()

            st.subheader("Answer")
            st.write(result.get("answer", "No answer found."))

            st.subheader("Sources")

            sources = result.get("sources", [])

            if not sources:
                st.info("No source documents found.")
            else:
                for source in sources:
                    st.write(
                        f"- {source.get('file', 'Unknown file')} "
                        f"(Page: "
                        f"{source.get('page') or 'N/A'})"
                    )

        except requests.RequestException as error:
            st.error(
                f"Question request failed: {error}"
            )
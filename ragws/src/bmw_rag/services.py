from bmw_rag.data_ingestors.chunkers import split_documents
from bmw_rag.data_ingestors.loaders import load_documents
from bmw_rag.settings import settings
from bmw_rag.vectordatabase.chroma_store import reset_collection


def reindex_documents() -> dict:
    settings.document_directory.mkdir(parents=True, exist_ok=True)

    documents, file_count = load_documents(
        settings.document_directory
    )

    if not documents:
        return {
            "files": 0,
            "chunks": 0,
            "message": "Add PDF or DOCX files to documents folder."
        }

    chunks = split_documents(
        documents,
        settings.chunk_size,
        settings.chunk_overlap,
    )

    vector_store = reset_collection()
    vector_store.add_documents(chunks)

    return {
        "files": file_count,
        "chunks": len(chunks),
        "message": "Documents indexed successfully."
    }
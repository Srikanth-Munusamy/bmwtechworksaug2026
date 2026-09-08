from pathlib import Path

from bmw_rag.data_ingestors.chunkers import split_documents
from bmw_rag.data_ingestors.loaders import load_documents
from bmw_rag.settings import settings
from bmw_rag.vectordatabase.chroma_store import reset_collection


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def reindex_documents(client: str) -> dict:
    client_name = client.strip().lower()

    document_directory = (
        PROJECT_ROOT
        / client_name
        / Path(settings.document_directory).name
    )
    document_directory.mkdir(parents=True, exist_ok=True)

    documents, file_count = load_documents(document_directory)

    if not documents:
        return {
            "client": client_name,
            "files": 0,
            "chunks": 0,
            "message": f"Add PDF or DOCX files to {document_directory}.",
        }

    chunks = split_documents(
        documents,
        settings.chunk_size,
        settings.chunk_overlap,
    )

    vector_store = reset_collection(client_name)
    vector_store.add_documents(chunks)

    return {
        "client": client_name,
        "files": file_count,
        "chunks": len(chunks),
        "stored_chunks": vector_store._collection.count(),
        "message": "Documents indexed successfully.",
    }
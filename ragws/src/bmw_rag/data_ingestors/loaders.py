from pathlib import Path

from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader
from langchain_core.documents import Document


def load_document(path: Path) -> list[Document]:
    if path.suffix.lower() == ".pdf":
        return PyPDFLoader(str(path)).load()

    if path.suffix.lower() == ".docx":
        return Docx2txtLoader(str(path)).load()

    raise ValueError(f"Unsupported document: {path.name}")


def load_documents(directory: Path) -> tuple[list[Document], int]:
    paths = [
        path for path in directory.rglob("*")
        if path.suffix.lower() in (".pdf", ".docx")
    ]

    documents = []

    for path in paths:
        documents.extend(load_document(path))

    return documents, len(paths)
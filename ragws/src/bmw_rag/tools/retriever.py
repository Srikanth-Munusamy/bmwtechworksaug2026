from bmw_rag.settings import settings
from bmw_rag.vectordatabase.chroma_store import get_vector_store


def retrieve(question: str):
    vector_store = get_vector_store()

    return vector_store.similarity_search(
        question,
        k=settings.number_of_chunks,
    )
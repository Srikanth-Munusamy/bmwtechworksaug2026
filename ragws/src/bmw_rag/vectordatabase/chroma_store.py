from langchain_aws import BedrockEmbeddings
from langchain_chroma import Chroma

from bmw_rag.settings import settings


def get_vector_store() -> Chroma:
    settings.vector_directory.mkdir(parents=True, exist_ok=True)

    return Chroma(
        collection_name=settings.collection_name,
        embedding_function=BedrockEmbeddings(
            model_id=settings.embedding_model,
            region_name=settings.aws_region,
        ),
        persist_directory=str(settings.vector_directory),
    )


def reset_collection() -> Chroma:
    store = get_vector_store()

    try:
        store.delete_collection()
    except ValueError:
        pass

    return get_vector_store()
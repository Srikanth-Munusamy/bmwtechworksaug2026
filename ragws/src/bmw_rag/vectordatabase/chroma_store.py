from pathlib import Path

from langchain_aws import BedrockEmbeddings
from langchain_chroma import Chroma

from bmw_rag.settings import settings


PROJECT_ROOT = Path(__file__).resolve().parents[3]


def get_vector_store(client: str) -> Chroma:
    client_name = client.strip().lower()

    vector_directory = (
        PROJECT_ROOT
        / client_name
        / Path(settings.vector_directory).name
    )

    vector_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return Chroma(
        collection_name=settings.collection_name,
        embedding_function=BedrockEmbeddings(
            model_id=settings.embedding_model,
            region_name=settings.aws_region,
        ),
        persist_directory=str(vector_directory),
    )


def reset_collection(client: str) -> Chroma:
    store = get_vector_store(client)

    try:
        store.delete_collection()
    except ValueError:
        pass

    return get_vector_store(client)
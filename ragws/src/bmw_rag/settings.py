import tomllib
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
#load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    document_directory: Path
    vector_directory: Path
    collection_name: str
    chunk_size: int
    chunk_overlap: int
    number_of_chunks: int
    embedding_model: str
    chat_model: str
    temperature: float
    aws_region: str
    api_host: str
    api_port: int
    api_base_url: str


def load_settings() -> Settings:
    with (PROJECT_ROOT / "config.toml").open("rb") as file:
        config = tomllib.load(file)

    return Settings(
        document_directory=PROJECT_ROOT / config["documents"]["directory"],
        vector_directory=PROJECT_ROOT / config["vector_database"]["directory"],
        collection_name=config["vector_database"]["collection_name"],
        chunk_size=config["chunking"]["chunk_size"],
        chunk_overlap=config["chunking"]["chunk_overlap"],
        number_of_chunks=config["retrieval"]["number_of_chunks"],
        embedding_model=config["models"]["embedding_model"],
        chat_model=config["models"]["chat_model"],
        temperature=config["models"]["temperature"],
        aws_region=config["aws"]["region"],
        api_host=config["api"]["host"],
        api_port=config["api"]["port"],
        api_base_url=config["api"]["base_url"],
    )


settings = load_settings()
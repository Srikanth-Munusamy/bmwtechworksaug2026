import os
import tomllib
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = (
    Path(__file__)
    .resolve()
    .parents[2]
)

load_dotenv(
    ROOT_DIR / ".env"
)


with open(
    ROOT_DIR / "config.toml",
    "rb"
) as f:

    CONFIG = tomllib.load(f)


OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

MODEL = CONFIG["agent"]["model"]

MAX_ITERATIONS = (
    CONFIG["agent"][
        "max_iterations"
    ]
)

AWS_REGION = (
    CONFIG["aws"]["region"]
)

S3_BUCKET = (
    CONFIG["s3"]["bucket"]
)

INVENTORY_KEY = (
    CONFIG["s3"][
        "inventory_key"
    ]
)

BACKEND_URL = (
    CONFIG["backend"][
        "base_url"
    ]
)
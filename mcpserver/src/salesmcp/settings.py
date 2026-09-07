import os
import tomllib
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")

with open(PROJECT_ROOT / "config.toml", "rb") as file:
    CONFIG = tomllib.load(file)


DATABASE_PATH = PROJECT_ROOT / CONFIG["database"]["path"]

MCP_HOST = CONFIG["mcp"]["host"]
MCP_PORT = CONFIG["mcp"]["port"]
MCP_URL = CONFIG["mcp"]["url"]

API_URL = CONFIG["api"]["url"]

MODEL = CONFIG["agent"]["model"]
TEMPERATURE = CONFIG["agent"]["temperature"]

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
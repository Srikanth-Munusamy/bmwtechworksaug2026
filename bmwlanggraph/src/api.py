from fastapi import FastAPI
from pydantic import BaseModel

from graph import run_graph


app = FastAPI(
    title="Inventory LangGraph API"
)


class InventoryRequest(BaseModel):
    question: str


@app.get("/")
def home():

    return {
        "message":
        "Inventory LangGraph API"
    }


@app.post("/inventory")
def inventory_agent(
    request: InventoryRequest
):

    answer = run_graph(
        request.question
    )

    return {
        "answer": answer
    }
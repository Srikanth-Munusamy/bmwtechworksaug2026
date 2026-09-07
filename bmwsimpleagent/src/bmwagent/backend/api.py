from fastapi import FastAPI
from pydantic import BaseModel

from bmwagent.backend.agent import (
    run_agent
)


app = FastAPI(
    title="BMW LangChain Agent API"
)


# -------------------------------------------------
# Request
# -------------------------------------------------

class AgentRequest(BaseModel):
    question: str


# -------------------------------------------------
# Home
# -------------------------------------------------

@app.get("/")
def home():

    return {
        "message":
            "BMW LangChain Agent API"
    }


# -------------------------------------------------
# Agent Endpoint
# -------------------------------------------------

@app.post("/agent/query")
def query_agent(
    request: AgentRequest
):

    result = run_agent(
        request.question
    )

    return result
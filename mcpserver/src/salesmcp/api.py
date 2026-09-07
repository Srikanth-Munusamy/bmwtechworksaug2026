from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from salesmcp.agent import run_agent


app = FastAPI(
    title="Sales MCP Agent API",
    version="1.0.0",
)

class AgentRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000,
    )


class AgentResponse(BaseModel):
    answer: str
    available_tools: list[str]

@app.get("/health")
def health():
    return {
        "status": "ok"
    }
@app.post(
    "/agent/query",
    response_model=AgentResponse,
)
async def query_agent(request: AgentRequest):

    try:
        result = await run_agent(
            request.question
        )

        return AgentResponse(**result)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error


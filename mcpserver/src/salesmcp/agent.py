from langchain.agents import create_agent

from langchain_mcp_adapters.client import (
    MultiServerMCPClient,
)

from langchain_openai import ChatOpenAI

from .settings import (
    MCP_URL,
    MODEL,
    OPENAI_API_KEY,
    TEMPERATURE,
)


AGENT_INSTRUCTIONS = """
You are a sales assistant.

Rules:
- Use MCP tools for product, order and sales facts.
- Never invent prices, stock, orders or revenue.
- Display monetary values in INR.
- Ask for explicit confirmation before creating an order.
- Call create_sales_order only after confirmation.
"""


async def run_agent(
    question: str,
    history: list[dict] | None = None,
) -> dict:

    if not OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY is missing"
        )

    # ---------------------------------------------
    # OpenAI LLM
    # ---------------------------------------------

    model = ChatOpenAI(
        model=MODEL,
        temperature=TEMPERATURE,
        api_key=OPENAI_API_KEY,
    )

    # ---------------------------------------------
    # MCP client configuration
    # ---------------------------------------------

    client = MultiServerMCPClient(
        {
            "sales": {
                "transport": "streamable_http",
                "url": MCP_URL,
            }
        }
    )

    # Discover tools from MCP server
    tools = await client.get_tools()

    print(
        "MCP tools:",
        [tool.name for tool in tools],
    )

    # ---------------------------------------------
    # Create LangChain agent
    # ---------------------------------------------

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=AGENT_INSTRUCTIONS,
    )

    messages = list(history or [])

    messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # This executes the LLM/tool-calling loop
    result = await agent.ainvoke(
        {
            "messages": messages
        }
    )

    final_message = result["messages"][-1]

    return {
        "answer": final_message.content,
        "available_tools": [
            tool.name for tool in tools
        ],
    }
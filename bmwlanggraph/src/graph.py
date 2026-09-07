from dotenv import load_dotenv
import os
from os import path
from langchain_openai import ChatOpenAI
from langchain.tools import tool

from langgraph.graph import (
    StateGraph,
    START,
    MessagesState
)

from langgraph.prebuilt import (
    ToolNode,
    tools_condition
)

env_path=path.join(path.dirname(__file__), ".env")
load_dotenv(env_path)

MODEL = os.getenv("MODEL", "gpt-5.6")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ------------------------------------
# Inventory Tool
# ------------------------------------

@tool
def get_inventory(item_name: str) -> str:
    """Get current inventory information for an item."""

    print(
        f"Inventory tool called: {item_name}"
    )

    inventory = {
        "brake_pad": {
            "quantity": 25,
            "reorder_level": 10
        },

        "battery_pack": {
            "quantity": 5,
            "reorder_level": 10
        },

        "air_filter": {
            "quantity": 40,
            "reorder_level": 15
        }
    }

    item = inventory.get(
        item_name.lower()
    )

    if item is None:
        return "Item not found"

    return (
        f"Item: {item_name}, "
        f"Quantity: {item['quantity']}, "
        f"Reorder Level: {item['reorder_level']}"
    )


# ------------------------------------
# LLM
# ------------------------------------

llm = ChatOpenAI(
    model=MODEL,
    api_key=OPENAI_API_KEY,
    use_responses_api=True
)


tools = [
    get_inventory
]


llm_with_tools = llm.bind_tools(
    tools
)


# ------------------------------------
# Agent Node
# ------------------------------------

def agent_node(state: MessagesState):

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# ------------------------------------
# Tool Node
# ------------------------------------

tool_node = ToolNode(
    tools
)


# ------------------------------------
# Build Graph
# ------------------------------------

builder = StateGraph(
    MessagesState
)


builder.add_node(
    "agent",
    agent_node
)


builder.add_node(
    "tools",
    tool_node
)


builder.add_edge(
    START,
    "agent"
)


builder.add_conditional_edges(
    "agent",
    tools_condition
)


builder.add_edge(
    "tools",
    "agent"
)


# ------------------------------------
# Compile
# ------------------------------------

graph = builder.compile()


# ------------------------------------
# Run Graph
# ------------------------------------

def run_graph(question: str):

    result = graph.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )

    final_message = result["messages"][-1]

    content = final_message.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        return "\n".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict)
            and block.get("type") == "text"
        )

    return str(content)
import os
import tomllib

from pathlib import Path

from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from bmwagent.backend.tools import get_vehicle_status


# -------------------------------------------------
# Paths
# -------------------------------------------------

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[3]
)

BMW_AGENT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)


# -------------------------------------------------
# Environment
# -------------------------------------------------

load_dotenv(
    PROJECT_ROOT / ".env"
)


# -------------------------------------------------
# Configuration
# -------------------------------------------------

CONFIG_FILE = (
    BMW_AGENT_ROOT / "config.toml"
)

with open(
    CONFIG_FILE,
    "rb"
) as file:

    CONFIG = tomllib.load(file)


MODEL = CONFIG["agent"]["model"]


# -------------------------------------------------
# OpenAI API Key
# -------------------------------------------------

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

if not OPENAI_API_KEY:

    raise ValueError(
        "OPENAI_API_KEY is not configured in .env"
    )


# -------------------------------------------------
# LLM
# -------------------------------------------------

llm = ChatOpenAI(

    model=MODEL,

    api_key=OPENAI_API_KEY,

    # Required for GPT-5.6 + tool calling
    use_responses_api=True
)


# -------------------------------------------------
# Agent Instructions
# -------------------------------------------------

AGENT_INSTRUCTIONS = """
You are a BMW Vehicle Diagnostic Agent.

Your job is to analyze BMW vehicle health.

Rules:

1. When the user asks about a vehicle,
   always use the get_vehicle_status tool.

2. Never invent vehicle information.

3. Vehicle information must come from
   get_vehicle_status.

4. Analyze the following:

   - vehicle ID
   - model
   - battery level
   - temperature
   - fault code
   - vehicle status

5. Classify the vehicle condition as:

   NORMAL
   WARNING
   CRITICAL

6. Give a short explanation.

7. Give a short recommendation.

8. If vehicle information is not available,
   clearly say that the vehicle was not found.

9. Do not invent missing values or units.

10. Keep the final response clear and concise.
"""


# -------------------------------------------------
# LangChain Agent
# -------------------------------------------------

agent = create_agent(

    model=llm,

    tools=[
        get_vehicle_status
    ],

    system_prompt=AGENT_INSTRUCTIONS
)


# -------------------------------------------------
# Run Agent
# -------------------------------------------------

def run_agent(
    question: str
) -> dict:

    # ---------------------------------------------
    # Validate input
    # ---------------------------------------------

    if not question:

        raise ValueError(
            "Question cannot be empty"
        )

    question = question.strip()

    if not question:

        raise ValueError(
            "Question cannot be empty"
        )


    print("\n===================================")
    print("BMW Agent Started")
    print("===================================")

    print(
        f"User Question: {question}"
    )


    # ---------------------------------------------
    # Invoke LangChain Agent
    # ---------------------------------------------

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )


    # ---------------------------------------------
    # Get messages
    # ---------------------------------------------

    messages = result.get(
        "messages",
        []
    )

    if not messages:

        raise RuntimeError(
            "Agent returned no messages"
        )


    # ---------------------------------------------
    # Final response
    # ---------------------------------------------

    final_message = messages[-1]


    # ---------------------------------------------
    # Extract text
    # ---------------------------------------------

    try:

        answer = final_message.text

    except Exception:

        answer = final_message.content


    # ---------------------------------------------
    # Count LLM iterations
    # ---------------------------------------------

    iterations = 0

    for message in messages:

        if getattr(
            message,
            "type",
            None
        ) == "ai":

            iterations += 1


    # ---------------------------------------------
    # Capture tools used
    # ---------------------------------------------

    tools_used = []


    for message in messages:

        if getattr(
            message,
            "type",
            None
        ) != "ai":

            continue


        tool_calls = getattr(
            message,
            "tool_calls",
            []
        )


        if not tool_calls:

            continue


        for tool_call in tool_calls:

            tools_used.append(
                {
                    "tool":
                        tool_call.get(
                            "name"
                        ),

                    "arguments":
                        tool_call.get(
                            "args",
                            {}
                        )
                }
            )


    # ---------------------------------------------
    # Console Output
    # ---------------------------------------------

    print("\nAgent Answer:")
    print(answer)

    print("\nIterations:")
    print(iterations)

    print("\nTools Used:")

    if tools_used:

        for tool in tools_used:

            print(
                f"Tool: {tool['tool']}"
            )

            print(
                f"Arguments: "
                f"{tool['arguments']}"
            )

    else:

        print(
            "No tools used"
        )


    print("\n===================================")
    print("BMW Agent Completed")
    print("===================================\n")


    # ---------------------------------------------
    # Return to FastAPI
    # ---------------------------------------------

    return {

        "answer":
            answer,

        "tools_used":
            tools_used,

        "iterations":
            iterations
    }
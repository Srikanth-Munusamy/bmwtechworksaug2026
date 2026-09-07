import json

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI()


# ---------------------------------------
# Tool 1
# ---------------------------------------

def check_inventory(item: str):

    inventory = {
        "battery_pack": {
            "quantity": 5,
            "reorder_level": 10
        }
    }

    return inventory.get(
        item,
        {"error": "Item not found"}
    )


# ---------------------------------------
# Tool 2
# ---------------------------------------

def create_purchase_request(
    item: str,
    quantity: int
):

    return {
        "status": "CREATED",
        "item": item,
        "quantity": quantity
    }


# ---------------------------------------
# Goal
# ---------------------------------------

goal = """
Ensure battery_pack inventory is sufficient.

If stock is below reorder level,
create a purchase request.

Finish when the goal is completed.
"""


# ---------------------------------------
# Agent Memory
# ---------------------------------------

history = []


# ---------------------------------------
# Autonomous Agent Loop
# ---------------------------------------

for iteration in range(5):

    print(
        f"\n--- Iteration {iteration + 1} ---"
    )

    prompt = f"""
You are an autonomous inventory agent.

GOAL:
{goal}

TOOLS AVAILABLE:

1. check_inventory
   Input: item

2. create_purchase_request
   Input: item, quantity

Previous actions and observations:

{history}

Decide the NEXT action required.

Return ONLY JSON.

Possible responses:

{{
    "action": "check_inventory",
    "item": "battery_pack"
}}

or

{{
    "action": "create_purchase_request",
    "item": "battery_pack",
    "quantity": 5
}}

or

{{
    "action": "finish",
    "message": "Goal completed"
}}
"""

    response = client.responses.create(
        model="gpt-5.6",
        input=prompt
    )

    decision_text = (
        response.output_text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    decision = json.loads(
        decision_text
    )

    print(
        "Agent Decision:",
        decision
    )

    action = decision["action"]


    # -----------------------------------
    # Check Inventory
    # -----------------------------------

    if action == "check_inventory":

        result = check_inventory(
            decision["item"]
        )

        print(
            "Tool Result:",
            result
        )

        history.append(
            {
                "action": action,
                "result": result
            }
        )


    # -----------------------------------
    # Create Purchase Request
    # -----------------------------------

    elif action == "create_purchase_request":

        result = create_purchase_request(
            decision["item"],
            decision["quantity"]
        )

        print(
            "Tool Result:",
            result
        )

        history.append(
            {
                "action": action,
                "result": result
            }
        )


    # -----------------------------------
    # Finish
    # -----------------------------------

    elif action == "finish":

        print(
            "\nFINAL:",
            decision["message"]
        )

        break
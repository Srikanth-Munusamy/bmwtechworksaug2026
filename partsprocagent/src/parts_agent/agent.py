import json

from openai import OpenAI

from .api_client import BackendAPI
from .config import (
    MODEL,
    MAX_ITERATIONS
)
from .s3_inventory import S3Inventory


class PartsProcurementAgent:

    def __init__(self):

        self.client = OpenAI()

        self.api = BackendAPI()

        self.inventory = S3Inventory()

        self.purchase_authorized = False

    # ---------------------------------------------
    # Tool definitions
    # ---------------------------------------------
    def build_tools(
        self,
        purchase_authorized=False
    ):

        tools = [
            {
                "type": "function",
                "name":
                    "get_service_job",
                "description":
                    "Get a service job "
                    "from the backend API.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "job_id": {
                            "type":
                                "string"
                        }
                    },
                    "required": [
                        "job_id"
                    ],
                    "additionalProperties":
                        False
                }
            },

            {
                "type": "function",
                "name":
                    "check_inventory",
                "description":
                    "Check local parts "
                    "inventory in AWS S3.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "part_number": {
                            "type":
                                "string"
                        },
                        "quantity": {
                            "type":
                                "integer"
                        }
                    },
                    "required": [
                        "part_number",
                        "quantity"
                    ],
                    "additionalProperties":
                        False
                }
            },

            {
                "type": "function",
                "name":
                    "get_suppliers",
                "description":
                    "Get supplier quotes "
                    "and recommend one.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "part_number": {
                            "type":
                                "string"
                        },
                        "priority": {
                            "type":
                                "string"
                        }
                    },
                    "required": [
                        "part_number",
                        "priority"
                    ],
                    "additionalProperties":
                        False
                }
            }
        ]

        if purchase_authorized:

            tools.append(
                {
                    "type": "function",
                    "name":
                        "create_purchase_request",
                    "description":
                        "Create an authorized "
                        "purchase request.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "job_id": {
                                "type":
                                    "string"
                            },
                            "supplier_id": {
                                "type":
                                    "string"
                            },
                            "part_number": {
                                "type":
                                    "string"
                            },
                            "quantity": {
                                "type":
                                    "integer"
                            },
                            "unit_price": {
                                "type":
                                    "number"
                            }
                        },
                        "required": [
                            "job_id",
                            "supplier_id",
                            "part_number",
                            "quantity",
                            "unit_price"
                        ],
                        "additionalProperties":
                            False
                    }
                }
            )

        return tools

    # ---------------------------------------------
    # Execute tool
    # ---------------------------------------------
    def execute_tool(
        self,
        name,
        args
    ):

        if name == "get_service_job":

            return self.api.get_job(
                args["job_id"]
            )

        if name == "check_inventory":

            return (
                self.inventory
                .check_inventory(
                    args[
                        "part_number"
                    ],
                    args["quantity"]
                )
            )

        if name == "get_suppliers":

            suppliers = (
                self.api.get_suppliers(
                    args[
                        "part_number"
                    ]
                )
            )

            if not suppliers:

                return {
                    "suppliers": [],
                    "recommended":
                        None
                }

            priority = (
                args["priority"]
                .upper()
            )

            # Urgent:
            # fastest delivery first
            if priority == "URGENT":

                suppliers = sorted(
                    suppliers,
                    key=lambda x: (
                        x[
                            "delivery_days"
                        ],
                        x[
                            "unit_price"
                        ]
                    )
                )

            # Normal:
            # lower cost first
            else:

                suppliers = sorted(
                    suppliers,
                    key=lambda x: (
                        x[
                            "unit_price"
                        ],
                        x[
                            "delivery_days"
                        ]
                    )
                )

            return {
                "suppliers":
                    suppliers,
                "recommended":
                    suppliers[0]
            }

        if (
            name
            == "create_purchase_request"
        ):

            if not self.purchase_authorized:

                return {
                    "error":
                    "Purchase not authorized"
                }

            return (
                self.api
                .create_purchase_request(
                    args
                )
            )

        return {
            "error":
            f"Unknown tool: {name}"
        }

    # ---------------------------------------------
    # Main agent loop
    # ---------------------------------------------
    def run(
        self,
        job_id: str,
        authorize_purchase=False
    ):

        self.purchase_authorized = (
            authorize_purchase
        )

        tools = self.build_tools(
            authorize_purchase
        )

        instructions = """
You are a BMW Parts Procurement AI Agent.

Rules:

1. Always call get_service_job first.

2. After retrieving the job,
   call check_inventory using the
   part_number and quantity returned
   by get_service_job.

3. If local inventory is available,
   use local inventory.
   Do not call get_suppliers.
   Do not create a purchase request.

4. If local inventory is unavailable,
   call get_suppliers.

5. Use the supplier returned as
   recommended by get_suppliers.

6. If create_purchase_request is
   available, create the purchase
   request using the recommended
   supplier.

7. Never invent a job, stock value,
   supplier, price, or delivery time.

8. Return a clear final summary with:
   Job
   Vehicle
   Part
   Quantity
   Priority
   Local Stock
   Supplier
   Price
   Delivery
   Action
"""

        input_items = [
            {
                "role": "user",
                "content":
                    f"Process service job "
                    f"{job_id}."
            }
        ]

        for _ in range(
            MAX_ITERATIONS
        ):

            response = (
                self.client
                .responses.create(
                    model=MODEL,
                    instructions=
                        instructions,
                    tools=tools,
                    input=input_items
                )
            )

            # Preserve model output
            input_items += (
                response.output
            )

            tool_calls = [
                item
                for item
                in response.output
                if item.type
                == "function_call"
            ]

            # No more tool calls:
            # final answer available
            if not tool_calls:

                return (
                    response.output_text
                )

            for call in tool_calls:

                args = json.loads(
                    call.arguments
                )

                result = (
                    self.execute_tool(
                        call.name,
                        args
                    )
                )

                input_items.append(
                    {
                        "type":
                            "function_call_output",
                        "call_id":
                            call.call_id,
                        "output":
                            json.dumps(
                                result
                            )
                    }
                )

        raise RuntimeError(
            "Agent reached maximum "
            "iterations"
        )
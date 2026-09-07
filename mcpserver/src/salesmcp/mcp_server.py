import json

from mcp.server.fastmcp import FastMCP

from salesmcp.settings import (
    MCP_HOST,
    MCP_PORT,
)

# Import the module, not individual functions.
from . import database


# -------------------------------------------------
# MCP server configuration
# -------------------------------------------------

mcp = FastMCP(
    name="Sales MCP Server",
    host=MCP_HOST,
    port=MCP_PORT,
    stateless_http=True,
    json_response=True,
)


# -------------------------------------------------
# Initialize database
# -------------------------------------------------

database.initialize_database()


# -------------------------------------------------
# MCP Tool 1: List products
# -------------------------------------------------

@mcp.tool()
def list_products(
    category: str | None = None,
) -> list[dict]:
    """
    List products, prices and available stock.

    Args:
        category:
            Optional product category.
    """

    return database.list_products(
        category=category
    )


# -------------------------------------------------
# MCP Tool 2: Get order
# -------------------------------------------------

@mcp.tool()
def get_order(
    order_id: int,
) -> dict:
    """
    Retrieve one sales order by order ID.

    Args:
        order_id:
            Numeric order identifier.
    """

    order = database.get_order(
        order_id=order_id
    )

    if order is None:
        return {
            "found": False,
            "message": (
                f"Order {order_id} was not found"
            ),
        }

    return {
        "found": True,
        "order": order,
    }


# -------------------------------------------------
# MCP Tool 3: Sales summary
# -------------------------------------------------

@mcp.tool()
def get_sales_summary(
    start_date: str,
    end_date: str,
) -> dict:
    """
    Calculate confirmed sales between two dates.

    Date format:
        YYYY-MM-DD
    """

    return database.sales_summary(
        start_date=start_date,
        end_date=end_date,
    )


# -------------------------------------------------
# MCP Tool 4: Create sales order
# -------------------------------------------------

@mcp.tool()
def create_sales_order(
    customer_name: str,
    product_id: int,
    quantity: int,
    user_confirmed: bool,
) -> dict:
    """
    Create a sales order after explicit confirmation.

    Args:
        customer_name:
            Customer placing the order.
        product_id:
            Product identifier.
        quantity:
            Number of units.
        user_confirmed:
            True only after explicit user confirmation.
    """

    if not user_confirmed:
        return {
            "created": False,
            "confirmation_required": True,
            "message": (
                "Ask the user to confirm customer name, "
                "product ID and quantity."
            ),
        }

    try:
        order = database.create_order(
            customer_name=customer_name,
            product_id=product_id,
            quantity=quantity,
        )

        return {
            "created": True,
            "message": (
                "Sales order created successfully"
            ),
            "order": order,
        }

    except ValueError as error:
        return {
            "created": False,
            "message": str(error),
        }


# -------------------------------------------------
# MCP Resource 1: Product catalog
# -------------------------------------------------

@mcp.resource("sales://catalog")
def product_catalog() -> str:
    """
    Provide the current product catalog.
    """

    products = database.list_products()

    return json.dumps(
        products,
        indent=2,
    )


# -------------------------------------------------
# MCP Resource 2: Order policy
# -------------------------------------------------

@mcp.resource(
    "sales://policy/order-creation"
)
def order_creation_policy() -> str:
    """
    Provide the sales-order creation policy.
    """

    return """
Create an order only after the user explicitly
confirms customer name, product ID and quantity.
Never assume user confirmation.
""".strip()


# -------------------------------------------------
# MCP Prompt: Sales analysis
# -------------------------------------------------

@mcp.prompt()
def analyze_sales(
    start_date: str,
    end_date: str,
) -> str:
    """
    Provide a reusable sales-analysis prompt.
    """

    return f"""
Analyze confirmed sales from
{start_date} through {end_date}.

Use the get_sales_summary tool.

Report:

1. Revenue
2. Units sold
3. Order count
4. Top-performing product

Do not invent missing sales information.
""".strip()


# -------------------------------------------------
# Run directly
# -------------------------------------------------

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http"
    )
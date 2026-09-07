from salesmcp.mcp_server import mcp
from salesmcp.settings import MCP_HOST, MCP_PORT
from salesmcp.mcp_server import mcp


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http"
    )
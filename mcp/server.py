from mcp.server.fastmcp import FastMCP
import uvicorn

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

# if __name__ == "__main__":
#     mcp.run(
#         transport="streamable-http",
#     )
http_app = mcp.streamable_http_app()

if __name__ == "__main__":
    uvicorn.run(http_app, host="0.0.0.0", port=5000)

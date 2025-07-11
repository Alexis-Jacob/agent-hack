from mcp.server.fastmcp import FastMCP
import uvicorn
from reddit_api.api import mcp
# mcp = FastMCP("Math")

# @mcp.tool()
# def add(a: int, b: int) -> int:
#     """Add two numbers."""
#     return a + b

# @mcp.tool()
# def multiply(a: int, b: int) -> int:
#     """Multiply two numbers."""
#     return a * b

# @mcp.tool()
# def what_is_my_name() -> str:
#     """Answer the question of what is my name"""
#     return "my name is alexis"




# if __name__ == "__main__":
#     mcp.run(
#         transport="streamable-http",
#     )
http_app = mcp.streamable_http_app()

if __name__ == "__main__":
    uvicorn.run(http_app, host="0.0.0.0", port=5000)

"""A small MCP tool host, run standalone or launched by tool_client.py over stdio."""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my_mcp-demo")


@mcp.tool()
async def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@mcp.tool()
async def echo(text: str) -> str:
    """Echo the given text back."""
    return text


if __name__ == "__main__":
    mcp.run()

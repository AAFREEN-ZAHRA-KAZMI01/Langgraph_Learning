from mcp.server.fastmcp import FastMCP

mcp = FastMCP("agenticai")


@mcp.tool()
async def greet(name: str) -> str:
    return f"Hello, {name}!"


if __name__ == "__main__":
    mcp.run()

"""LangGraph node that calls a tool exposed by tool_host.py over MCP stdio."""
import asyncio
import sys
from pathlib import Path

from langgraph.graph import StateGraph
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

HOST_SCRIPT = Path(__file__).parent / "tool_host.py"
SERVER_PARAMS = StdioServerParameters(command=sys.executable, args=[str(HOST_SCRIPT)])


# Step 1-2: connect to the tool host, call the "add" tool with the graph state
async def invoke_add_tool(state):
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("add", {"a": state["a"], "b": state["b"]})
            return {**state, "result": result.structuredContent["result"]}


# Step 3: build a single-node LangGraph graph around the tool call
builder = StateGraph(dict)
builder.add_node("invoke_add_tool", invoke_add_tool)
builder.set_entry_point("invoke_add_tool")
builder.set_finish_point("invoke_add_tool")
graph = builder.compile()


# Step 4: run it
async def main():
    result = await graph.ainvoke({"a": 2, "b": 3})
    print("Output:", result["result"])


if __name__ == "__main__":
    asyncio.run(main())

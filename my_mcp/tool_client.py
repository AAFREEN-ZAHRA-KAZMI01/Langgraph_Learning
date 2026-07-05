from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from mcp import MCPClient

# Step 1: Connect to tool host (default localhost:8080)
client = MCPClient()  # or MCPClient(base_url="http://localhost:8080")

# Step 2: Fetch the tool
tools = client.list_tools()
print("Tools available:", tools)

# Step 3: Use tool with LangGraph ToolExecutor
tool_executor = ToolExecutor([client])

# Step 4: Define graph state and node

# State is just a dictionary for now
def invoke_tool(state):
    result = tool_executor.invoke({"input": state["input"]})
    return {"input": result["output"]}

# Step 5: Build the LangGraph
builder = StateGraph(dict)

builder.add_node("invoke_tool", invoke_tool)
builder.set_entry_point("invoke_tool")
builder.set_finish_point("invoke_tool")

graph = builder.compile()

# Step 6: Run it!
result = graph.invoke({"input": "Abdullah"})
print("Output:", result["input"])

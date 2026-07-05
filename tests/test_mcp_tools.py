import asyncio


def test_main_greet_tool():
    import main as main_module

    async def run():
        return await main_module.mcp.call_tool("greet", {"name": "World"})

    _content, structured = asyncio.run(run())
    assert structured["result"] == "Hello, World!"


def test_tool_host_add():
    from my_mcp import tool_host

    async def run():
        return await tool_host.mcp.call_tool("add", {"a": 2, "b": 3})

    _content, structured = asyncio.run(run())
    assert structured["result"] == 5.0


def test_tool_host_echo():
    from my_mcp import tool_host

    async def run():
        return await tool_host.mcp.call_tool("echo", {"text": "hi"})

    _content, structured = asyncio.run(run())
    assert structured["result"] == "hi"

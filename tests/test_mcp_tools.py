import asyncio
from unittest.mock import MagicMock, patch


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


def test_tool_host_summarize_text():
    from my_mcp import tool_host

    async def run():
        with patch.object(tool_host, "llm", return_value=MagicMock(content="short summary")):
            return await tool_host.mcp.call_tool("summarize_text", {"text": "a very long text..."})

    _content, structured = asyncio.run(run())
    assert structured["result"] == "short summary"


def test_tool_host_send_email_tool():
    from my_mcp import tool_host

    async def run():
        with patch.object(tool_host, "send_email", return_value=True) as mock_send:
            result = await tool_host.mcp.call_tool(
                "send_email_tool", {"subject": "s", "body": "b", "to_email": "x@example.com"}
            )
            return result, mock_send

    (_content, structured), mock_send = asyncio.run(run())
    assert structured["result"] == "Email sent successfully."
    mock_send.assert_called_once_with("s", "b", "x@example.com")

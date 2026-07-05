"""An MCP tool host, run standalone or launched by tool_client.py over stdio.

Exposes a couple of toy tools (add, echo) plus two that wrap real
functionality from 1-tool-integration/, so an MCP client can trigger an
email send or ask the Groq LLM for a summary.
"""
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "1-tool-integration"))

from email_utils import get_llm, send_email  # noqa: E402
from langchain.schema import HumanMessage  # noqa: E402

mcp = FastMCP("my_mcp-demo")
llm = get_llm()


@mcp.tool()
async def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@mcp.tool()
async def echo(text: str) -> str:
    """Echo the given text back."""
    return text


@mcp.tool()
async def summarize_text(text: str) -> str:
    """Summarize the given text using the Groq LLM."""
    prompt = f"Summarize this text in a few sentences:\n\n{text}"
    return llm([HumanMessage(content=prompt)]).content


@mcp.tool()
async def send_email_tool(subject: str, body: str, to_email: str) -> str:
    """Send an email via Gmail SMTP. Returns a success/failure message."""
    ok = send_email(subject, body, to_email)
    return "Email sent successfully." if ok else "Failed to send email."


if __name__ == "__main__":
    mcp.run()

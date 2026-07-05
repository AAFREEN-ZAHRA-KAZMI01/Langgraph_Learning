import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL_DIR = ROOT / "1-tool-integration"

for path in (ROOT, TOOL_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

# Dummy values so importing modules that construct API clients at import
# time (ChatGroq, NotionClient) doesn't require real secrets in CI.
os.environ.setdefault("GROQ_API_KEY", "dummy-groq-key")
os.environ.setdefault("EMAIL_ADDRESS", "dummy@example.com")
os.environ.setdefault("EMAIL_PASSWORD", "dummy-password")
os.environ.setdefault("NOTION_API_KEY", "dummy-notion-key")

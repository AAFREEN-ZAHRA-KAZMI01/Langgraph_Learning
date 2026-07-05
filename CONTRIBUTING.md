# Contributing

This is a personal learning repo, but if you're picking it up (including future-me), here's how to work in it.

## Setup

```bash
git clone https://github.com/AAFREEN-ZAHRA-KAZMI01/Langgraph_Learning.git
cd Langgraph_Learning
uv sync --group dev
cp .env.example .env   # fill in your own keys
```

Prefer `pip install -r requirements.txt` if you're not using `uv`.

## Before committing

```bash
uv run ruff check .      # lint
uv run pytest            # run the test suite
```

Both also run in CI on every push/PR to `main` (`.github/workflows/ci.yml`).

## Guidelines

- **Never commit secrets.** `.env`, `LangChain-GoogleDocs/credentials.json`, and `LangChain-GoogleDocs/token.pickle` are gitignored — keep it that way. If you add a new integration that needs a credential file or API key, add it to `.env.example` (placeholder only) and to `.gitignore` if it's a file.
- **Shared logic goes in a `*_utils.py` module**, not copy-pasted across scripts. See `1-tool-integration/email_utils.py` for the pattern the email/WhatsApp tools follow.
- **Naming**: folders use the `N-name` convention (e.g. `1-tool-integration`, `1-multichatbot`); avoid mixing in `N.name`.
- **Separate I/O from logic.** A function that needs a value (a topic, a page ID, a count) should take it as a parameter and return a result — don't call `input()`/`print()` inside it. Put the `input()`/`print()` calls in a thin CLI wrapper instead. This is what makes the same function reusable from the CLI, `webapp/app.py`, and `my_mcp/tool_host.py`, and testable without mocking stdin. See `notion_tool.py`'s `generate_document_content()` vs `generate_new_document()` for the pattern.
- Keep new tool scripts runnable standalone (`python path/to/script.py`) and add a corresponding test under `tests/` that mocks any external API/network call.
- Check the [Groq deprecations page](https://console.groq.com/docs/deprecations) if an LLM call suddenly starts failing with `model_decommissioned` — Groq retires models over time.

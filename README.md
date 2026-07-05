# 🤖 LangGraph Learning — Aafreen Zahra Kazmi

Welcome to **LangGraph Learning**, where I explore and implement different AI agent-based architectures using **LangChain**, **LangGraph**, **MCP**, streaming, and tool integrations. This repository is structured in phases, starting from basic chatbot concepts to multi-agent systems and real-world tool integrations (email, Notion, Google Docs) powered by **Groq's LLaMA3**.

---

## 📌 Table of Contents

- [🔍 About the Project](#-about-the-project)
- [📁 Folder Structure](#-folder-structure)
- [🧠 Architectures Overview](#-architectures-overview)
- [🛠️ Tool Integrations](#️-tool-integrations)
- [⚙️ Setup & Installation](#️-setup--installation)
- [🔐 Environment Variables](#-environment-variables)
- [▶️ How to Run](#️-how-to-run)
- [📌 Future Work](#-future-work)
- [📬 Contact](#-contact)

---

## 🔍 About the Project

This repository is my personal LangGraph learning journey. It explores:
- Streaming chatbots with memory
- Multi-agent collaboration (simple, supervisor, hierarchical)
- Tool integration: Gmail, Notion, WhatsApp/Twilio, Google Drive/Docs
- MCP (Model Context Protocol) tool host/client examples
- Groq's fast LLaMA3 models via LangChain

---

## 📁 Folder Structure

```bash
AGENTICAI/
│
├── 1-BasicChatbot/
│   └── 1-basicchatbot.ipynb            # Streaming chatbot with memory + tool calling
│
├── 1-multichatbot/
│   ├── simpleaagentarchitecture.ipynb        # Linear: researcher -> writer
│   ├── supervised_multiaiagents.ipynb        # Supervisor dynamically routes tasks
│   └── Simple_Hierarchical_Multi-Agent_System.ipynb  # CEO -> team leads -> agents
│
├── 1.tool_integration/
│   ├── fetch_email_tool.py             # Inbox summary, keyword search, auto-reply bot
│   ├── send_email_tool.py              # Send LLM replies via Gmail SMTP + LangSmith tracing
│   ├── send_email_with_langsmith.py.py # Standalone chat + email + LangSmith tracing demo
│   ├── notion_tool.py                  # Generate/summarize docs and save to Notion
│   └── whatsapp_tool.py                # WhatsApp/Twilio integration (WIP)
│
├── LangChain-GoogleDocs/
│   ├── google_drive_loader.py          # Download + summarize a Google Doc via service account
│   ├── requirements1.txt
│   ├── credentials.json                # Google service-account key (gitignored, not tracked)
│   └── token.pickle                    # OAuth session cache (gitignored, not tracked)
│
├── my_mcp/
│   ├── tool_host.py                    # MCP tool host (currently empty scaffold)
│   └── tool_client.py                  # LangGraph node that calls an MCP tool via MCPClient
│
├── main.py                             # Minimal MCP tool example (`greet`)
├── pyproject.toml / requirements.txt / uv.lock
├── .env.example                        # Template for required environment variables
└── README.md
```

---

## 🧠 Architectures Overview

### 1. Basic Streaming Chatbot (`1-BasicChatbot/`)
- LangGraph's built-in streaming
- Memory types: `ConversationBufferMemory`, `ConversationSummaryMemory`
- ReAct agent with a Tavily web search tool and a custom multiplication tool

### 2. Multi-Agent Architectures (`1-multichatbot/`)
- **Simple**: `Start → Researcher → Writer → End`
- **Supervisor**: `Start → Supervisor → [Researcher / Writer / Analyst] → Supervisor → End`
- **Hierarchical**: CEO → Research/Writing team leads → individual agents

---

## 🛠️ Tool Integrations (`1.tool_integration/`, `LangChain-GoogleDocs/`, `my_mcp/`)

| File | What it does |
|---|---|
| `fetch_email_tool.py` | IMAP inbox summary, keyword search, and an LLM-judged auto-reply bot over Gmail |
| `send_email_tool.py` | Sends LLM-generated replies via Gmail SMTP, traced with LangSmith |
| `send_email_with_langsmith.py.py` | Standalone chatbot that optionally emails its response, with LangSmith tracing |
| `notion_tool.py` | Generates documents with the LLM and saves/summarizes Notion pages |
| `whatsapp_tool.py` | Twilio/WhatsApp integration (work in progress) |
| `google_drive_loader.py` | Downloads a Google Doc via a service account and summarizes it |
| `my_mcp/tool_client.py` | LangGraph node that calls a tool exposed by an MCP host |
| `main.py` | Minimal MCP tool (`greet`) run via `mcp.core.run` |

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/AAFREEN-ZAHRA-KAZMI01/Langgraph_Learning.git
cd Langgraph_Learning
```

### 2. Create a virtual environment
```bash
python -m venv .venv
```

### 3. Activate it
- **Windows**: `.venv\Scripts\activate`
- **Mac/Linux**: `source .venv/bin/activate`

### 4. Install dependencies
```bash
pip install -r requirements.txt
# or, if using uv:
uv sync
```

---

## 🔐 Environment Variables

Copy [`.env.example`](.env.example) to `.env` and fill in your own values:

```bash
cp .env.example .env
```

| Variable | Used by | Notes |
|---|---|---|
| `GROQ_API_KEY` | all LLM calls | Groq API key |
| `EMAIL_ADDRESS` / `EMAIL_PASSWORD` | email tools | Use a Gmail **App Password**, not your real password |
| `SMTP_SERVER` / `SMTP_PORT` | `fetch_email_tool.py` | Optional, defaults to Gmail SMTP |
| `LANGCHAIN_API_KEY` / `LANGCHAIN_PROJECT` / `LANGCHAIN_ENDPOINT` | LangSmith tracing | Optional but recommended for debugging traces |
| `NOTION_API_KEY` | `notion_tool.py` | Notion integration secret |
| `TAVILY_API_KEY` | chatbot notebooks | Web search tool |

For `LangChain-GoogleDocs/google_drive_loader.py`, you also need a Google **service-account** `credentials.json` placed at `LangChain-GoogleDocs/credentials.json`. This file is not tracked in git (it contains a secret) — generate your own from the [Google Cloud Console](https://console.cloud.google.com/).

> ⚠️ Never commit `.env`, `credentials.json`, or `token.pickle`. All three are gitignored.

---

## ▶️ How to Run

```bash
python main.py
python 1.tool_integration/fetch_email_tool.py
python 1.tool_integration/send_email_tool.py
python 1.tool_integration/notion_tool.py
python LangChain-GoogleDocs/google_drive_loader.py
```

Notebooks under `1-BasicChatbot/` and `1-multichatbot/` can be run in Jupyter/VS Code.

---

## 📌 Future Work

- [ ] Add a web interface using Streamlit
- [ ] Finish the WhatsApp/Twilio tool
- [ ] Flesh out the MCP tool host (`my_mcp/tool_host.py`)
- [ ] Add more LangGraph agents (planner, critic, memory agent)

---

## 📬 Contact

Made with ❤️ by [Aafreen Zahra Kazmi](https://github.com/AAFREEN-ZAHRA-KAZMI01)
For queries: ✉️ [aafreenzk1214@gmail.com](mailto:aafreenzk1214@gmail.com)

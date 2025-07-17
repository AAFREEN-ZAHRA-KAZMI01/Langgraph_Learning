# Langgraph_Learning
````markdown
# 🤖 LangGraph Learning — Aafreen Zahra Kazmi

Welcome to **LangGraph Learning**, where I explore and implement different AI agent-based architectures using **LangChain**, **LangGraph**, **streaming**, **tool integrations**, and more. This repository is structured in phases, starting from basic chatbot concepts to advanced multi-agent systems using **Groq's LLaMA3** and LangChain agents.

---

## 📌 Table of Contents

- [🔍 About the Project](#-about-the-project)
- [📁 Folder Structure](#-folder-structure)
- [🧠 Architectures Overview](#-architectures-overview)
  - [1. Basic Streaming Chatbot](#1-basic-streaming-chatbot)
  - [2. Multi-Agent Architectures](#2-multi-agent-architectures)
  - [3. Tool Integration](#3-tool-integration)
- [⚙️ Setup & Installation](#️-setup--installation)
- [▶️ How to Run](#️-how-to-run)
- [🔐 Environment Variables](#-environment-variables)
- [📌 Future Work](#-future-work)
- [📬 Contact](#-contact)

---

## 🔍 About the Project

This repository is my personal LangGraph learning journey. It explores:
- Streaming chatbot creation
- Using built-in LangGraph memory features
- Multiple AI agent collaboration
- Email tool integration
- Groq’s blazing-fast LLaMA3 models

> Built entirely using **Python + LangChain + LangGraph + Groq + Email SMTP tools**

---

## 📁 Folder Structure

```bash
Langgraph_Learning/
│
├── 1_Basic_Chatbot/                 # Simple streaming chatbot with memory
│   ├── main.py                      # Basic chatbot logic
│   └── memory_streaming.py         # Streaming + Memory saver example
│
├── 2_Multi_AI_Agent/               # Three types of multi-agent architectures
│   ├── simple_multi_agent.py       # Linear pipeline: researcher → writer
│   ├── supervisor_multi_agent.py   # Supervisor chooses the right agent
│   └── hierarchical_multi_agent.py # Hierarchical agents with team leads
│
├── 3_Tool_Integration/             
│   └── email_tool_agent.py         # Email sending using agent and SMTP
│
├── requirements.txt                # All dependencies listed
├── .env                            # Secret keys (Groq API, SMTP, etc.)
└── README.md
````

---

## 🧠 Architectures Overview

### 1. Basic Streaming Chatbot
This chatbot uses:
- ✅ LangGraph's **built-in streaming**
- ✅ Multiple **memory types** for context:
  - `ConversationBufferMemory`
  - `ConversationSummaryMemory`
- ✅ **Tool Calling** with ReAct agent:
  - 🌐 **Web Search Tool** using `Tavily`
  - ➗ **Custom Multiplication Tool**
- ✅ Uses **ReAct agent executor** to decide tool usage
---

### 2. Multi-Agent Architectures

#### a. `simple_multi_agent.py` — Linear Flow

```text
Start → Researcher → Writer → End
```

* Each step is defined as a node in LangGraph.
* Fixed pipeline, perfect for small static tasks.

---

#### b. `supervisor_multi_agent.py` — Dynamic Supervisor Logic

```text
Start → Supervisor → [Researcher / Writer / Analyst] → Supervisor → End
```

* The **supervisor agent** dynamically routes tasks.
* Can handle flexible requests like:

  * "Do market research"
  * "Write summary"
  * "Analyze technical data"

---

#### c. `hierarchical_multi_agent.py` — Full Organization Tree

**Simple Hierarchical Multi-Agent System using Groq**

```text
CEO
├── Research Team Leader
│   ├── Data Researcher
│   └── Market Researcher
└── Writing Team Leader
    ├── Technical Writer
    └── Summary Writer
```

* The CEO handles high-level tasks.
* Each team lead delegates sub-tasks to agents below them.
* Mimics a real-world organization chart.

---

### 3. Tool Integration (Email)

* `email_tool_agent.py` uses **LangChain Tool Invocation**.
* It integrates **Gmail SMTP** to send chatbot responses directly to a user email.
* Uses secure `.env` to store sensitive credentials.

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/AAFREEN-ZAHRA-KAZMI01/Langgraph_Learning.git
cd Langgraph_Learning
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

* **Windows**:

  ```bash
  venv\Scripts\activate
  ```
* **Mac/Linux**:

  ```bash
  source venv/bin/activate
  ```

### 4. Install Requirements

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

Choose any file from the folders and run it with:

```bash
python filename.py
```

Examples:

```bash
python 1_Basic_Chatbot/main.py
python 2_Multi_AI_Agent/supervisor_multi_agent.py
python 3_Tool_Integration/email_tool_agent.py
```

---

## 🔐 Environment Variables

Create a `.env` file in the root folder like this:

```env
GROQ_API_KEY=your_groq_key_here
EMAIL=your_email_here
APP_PASSWORD=your_app_password
TAVILY_API_KEY=your_tavily_key_here
```

> ⚠️ Do **NOT** share these keys publicly. Always use `.env` file for secret keys.

---

## 📌 Future Work

* [ ] Add Web Interface using **Streamlit**
* [ ] Add **Voice Input** using OpenAI Whisper
* [ ] Integrate Google Calendar or Notion tool
* [ ] Add more LangGraph agents (planner, critic, memory agent)

---

## 📬 Contact

Made with ❤️ by [Aafreen Zahra Kazmi](https://github.com/AAFREEN-ZAHRA-KAZMI01)
For queries: ✉️ [aafreenzk1214@gmail.com](mailto:aafreenzk1214@gmail.com)

---

## ⭐️ Show some love!

If you liked this repo:

* Give it a ⭐️ star
* Fork it for learning
* Share with AI enthusiasts 🚀



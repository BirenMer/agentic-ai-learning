# Supervisor Agent with Agent-as-Tools Architecture

This folder implements a supervisor agent system where specialized agents (math and research) are exposed as tools for the supervisor, using LangChain, LangGraph, and OpenAI's GPT-4o.

## Overview

The architecture allows the supervisor agent to invoke other agents as callable tools, enabling modular and flexible workflows. Each agent is designed for a specific domain and can be reused or extended independently.

### Main Components

- **Supervisor Agent** (`supervisor_agent.py`):
  - Manages workflow and delegates tasks to math and research agents, which are used as tools.
  - Uses a custom prompt and can be configured for different output modes.

- **Research Agent** (`research_agent.py`):
  - Finds and analyzes information from the web using the Tavily search tool.
  - Exposed as a tool for the supervisor to call for research tasks.

- **Math Agent** (`math_agent.py`):
  - Solves mathematical problems and calculations using a calculator tool.
  - Exposed as a tool for the supervisor to call for math tasks.

- **Tools** (`tools.py`):
  - Provides web search, calculator, and basic math functions for agent use.

## How It Works

1. The supervisor receives a user request and decides which agent-tool to invoke (math or research).
2. The selected agent processes the request and returns results to the supervisor.
3. The supervisor manages the workflow until the task is complete.

## Usage

Run the supervisor agent or invoker scripts to start a sample workflow:

```bash
python3 invoke_supervisor_agent.py
```

Or run math/research agent invokers for isolated tests:

```bash
python3 invoke_math_agent.py
python3 invoke_research_agent.py
```

## Extensibility

- Add new agent-tools by extending the modules.
- Modify supervisor logic for custom workflows.

## Requirements

- Python 3.10+
- LangChain, LangGraph, OpenAI, Tavily, dotenv

Install dependencies using Poetry:

```bash
poetry install
```

---
For more details, see the source code in each module.

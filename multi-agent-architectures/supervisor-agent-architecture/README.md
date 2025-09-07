
# Supervisor Agent Architecture

This folder implements a supervisor agent system that coordinates specialized agents for research and math tasks, using LangChain, LangGraph, and OpenAI's GPT-4o.

## Overview

The architecture features a supervisor agent that delegates tasks to two specialized agents: a research agent and a math agent. Each agent uses dedicated tools and follows strict instructions for collaboration.

### Main Components

- **Supervisor Agent** (`supervisor_agent.py`):
	- Manages workflow and delegates tasks to research and math agents.
	- Ensures only one agent acts at a time and collects results.

- **Research Agent** (`research_agent.py`):
	- Handles web search and research tasks using the Tavily tool.
	- Responds only with research results.

- **Math Agent** (`math_agent.py`):
	- Performs math operations (add, multiply, divide) using custom tools.
	- Responds only with calculation results.

- **Tools** (`tools.py`):
	- Provides web search and basic math functions as agent tools.

## How It Works

1. The supervisor receives a user request and decides whether it is a research or math task.
2. The appropriate agent is assigned the task and returns results to the supervisor.
3. The supervisor manages the workflow until the task is complete.

## Usage

Run the supervisor agent or invoker scripts to start a sample workflow:

```bash
python3 invoke_supervisor_agent.py
```

or run math/research agent invokers for isolated tests:

```bash
python3 invoke_math_agent.py
python3 invoke_research_agent.py
```

## Extensibility

- Add new agents or tools by extending the modules.
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

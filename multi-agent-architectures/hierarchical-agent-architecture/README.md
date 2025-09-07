# Hierarchical Agent Architecture

This folder implements a modular, hierarchical agent system for research and document writing using LangChain, LangGraph, and OpenAI's GPT-4o.

## Overview

The architecture consists of multiple specialized agents coordinated by a supervisor node. Each agent is responsible for a distinct task, enabling collaborative workflows and extensibility.

### Main Components

- **Supervisor Node** (`root_node_supervisor_agent.py`):
	- Routes tasks between research and writing teams.
	- Uses LLM-based logic to manage agent collaboration.

- **Research Agent** (`research_agent.py`):
	- Performs web search and scraping using custom tools.
	- Returns research results to the supervisor.

- **Document Agent** (`document_agent.py`):
	- Handles document creation, editing, and reading.
	- Uses outline-based workflows for structured writing.

- **Utilities** (`helper_utils.py`):
	- Provides routing and state management for agents.

- **Tools** (`tools.py`):
	- Implements web scraping, search, document editing, and Python REPL tools for agent use.

## How It Works

1. The supervisor receives a user request and decides which team (research or writing) should act next.
2. The research agent gathers information using search and scraping tools.
3. The document agent writes or edits documents based on outlines and research results.
4. All agents report back to the supervisor, which manages the workflow until completion.

## Usage

Run the main invoker script to start a sample workflow:

```bash
python3 invoker_hierarchical_supervisor_node.py
```

This will stream the agent interactions for a sample research and writing task.

## Extensibility

- Add new agents or tools by extending the existing modules.
- Modify the supervisor logic for custom workflows.

## Requirements

- Python 3.10+
- LangChain, LangGraph, OpenAI, Tavily, dotenv

Install dependencies using Poetry:

```bash
poetry install
```

---
For more details, see the source code in each module.


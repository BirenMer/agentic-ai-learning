
# Network Agent Architecture

This folder implements a networked multi-agent system for collaborative tasks such as research and chart generation, using LangChain, LangGraph, and OpenAI's GPT-4o.

## Overview

Agents in this architecture work together by passing control and information through a graph structure. Each agent specializes in a particular function, enabling complex workflows.

### Main Components

- **Agent Graph** (`agent.py`):
	- Defines the agent workflow using a state graph.
	- Adds nodes for research and chart generation, and connects them.

- **Nodes** (`nodes.py`):
	- Implements the logic for each agent node (e.g., researcher, chart generator).
	- Uses system prompts to coordinate agent collaboration and task completion.

- **Tools** (`tools.py`):
	- Provides tools for web search (Tavily) and Python code execution (for chart generation).

- **Invoker** (`invoke.py`):
	- Runs a sample workflow, streaming agent interactions for a user query.

## How It Works

1. The user provides a task (e.g., "Get India's GDP over the past 5 years and make a line chart").
2. The research agent gathers the required data using search tools.
3. The chart generator agent creates a chart using Python code execution.
4. Agents communicate and pass control until the final answer is produced.

## Usage

Run the invoker script to start a sample workflow:

```bash
python3 invoke.py
```

This will stream the agent interactions for the provided task.

## Extensibility

- Add new agent nodes or tools by extending the modules.
- Modify the graph structure for custom workflows.

## Requirements

- Python 3.10+
- LangChain, LangGraph, OpenAI, Tavily, dotenv

Install dependencies using Poetry:

```bash
poetry install
```

---
For more details, see the source code in each module.

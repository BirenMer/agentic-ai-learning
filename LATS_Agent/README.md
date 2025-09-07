# LATS Agent

This folder contains the implementation of the LATS (Learning Agent Trajectory Search) Agent, designed for advanced agentic reasoning and solution trajectory exploration.

## Overview

The LATS Agent leverages a graph-based approach to roll out agent steps, evaluate solution nodes, and extract optimal trajectories for complex queries. It is suitable for tasks requiring multi-step reasoning, reflection, and strategy proposal.

### Main Components

- **Agent Graph** (`lats_agent_graph.py`):
  - Defines the agent's reasoning graph and step expansion logic.
  - Supports streaming of agent steps and solution node evaluation.

- **Invoker Script** (`invoke_last_agent_query_2.py`):
  - Demonstrates how to query the agent with a complex question.
  - Streams each step, prints rollout details, and extracts the best solution trajectory.

## How It Works

1. The agent graph receives a user question and streams step-by-step reasoning.
2. Each step is rolled out, and the height of the root node is printed for progress tracking.
3. After all steps, the best solution node is selected and its trajectory is extracted and displayed.

## Example Usage

Run the invoker script to see the agent in action:

```bash
python3 invoke_last_agent_query_2.py
```

This will output the agent's reasoning steps and the final best solution trajectory for the given question.

## Extensibility

- Extend the agent graph for new reasoning strategies or domains.
- Customize the invoker script for different queries or output formats.

## Requirements

- Python 3.10+
- Any dependencies listed in `pyproject.toml` or `poetry.lock`

Install dependencies using Poetry:

```bash
poetry install
```

---
For more details, see the source code in each module.

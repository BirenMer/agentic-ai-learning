# Reflexion Agent

This folder contains the implementation of the Reflexion Agent, designed for iterative reasoning, self-reflection, and answer revision using LangChain and LangGraph.

## Overview

The Reflexion Agent architecture enables agents to answer questions, reflect on their responses, and revise answers through a graph-based workflow. It supports multi-step reasoning and tool usage for improved solution quality.

### Main Components

- **Agent Graph** (`reflexion_agent_graph.py`):
  - Defines the graph structure for answering, reflecting, and revising.
  - Manages the event loop and agent transitions.

- **Chains** (`chains.py`):
  - Implements the first responder and revisor chains for generating and revising answers.

- **Execution Tools** (`execution_tools.py`):
  - Handles tool execution and integration with agent responses.

- **Schemas** (`schema.py`):
  - Defines the data structures for agent actions and tool calls.

- **Invoker Script** (`invoke_reflexion_agent.py`):
  - Demonstrates how to query the agent and print the final response.

## How It Works

1. The agent receives a question and generates an initial answer.
2. The agent reflects on its answer and proposes revisions if needed.
3. Tool calls are executed as required, and the process iterates for improved results.
4. The final answer is returned after a set number of iterations or when no further revisions are needed.

## Example Usage

Run the invoker script to see the agent in action:

```bash
python3 reflexion_agent/invoke_reflexion_agent.py
```

This will output the agent's reasoning steps and the final answer for the given question.

## Extensibility

- Extend the agent graph for new reasoning strategies or domains.
- Add new tools or revise the chains for custom workflows.

## Requirements

- Python 3.10+
- LangChain, LangGraph, OpenAI, dotenv

Install dependencies using Poetry:

```bash
poetry install
```

---
For more details, see the source code in each module.

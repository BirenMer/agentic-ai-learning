# Basic **Reflection** Agent

This folder contains a simple implementation of a reflexion agent, designed to demonstrate basic agentic reasoning, chain execution, and schema management using LangChain and Python.

## Overview

The basic reflexion agent architecture enables agents to execute tasks, manage state, and utilize tools for reasoning and reflection. It serves as a foundation for more advanced agentic workflows.

### Main Components

- **Core Agent Logic** (`basic.py`):

  - Implements the main agent workflow and reasoning steps.
- **Chains** (`chains.py`):

  - Defines chains for sequential task execution and agent actions.
- **Schema** (`schema.py`):

  - Provides data structures for agent state and message passing.
- **Execution Tools** (`execution_tools.py`):

  - Supplies utility functions and tools for agent operations.

## How It Works

1. The agent receives a task or question.
2. Chains are executed to process the input and generate responses.
3. The agent manages state and uses tools as needed for reasoning and reflection.
4. The final result is returned after processing.

## Example Usage

Run the main agent script to see basic reflexion logic in action:

```bash
python3 basic_reflex_agent/basic.py
```

## Extensibility

- Add new chains or tools for more complex reasoning.
- Extend schema definitions for advanced agent state management.

## Requirements

- Python 3.10+
- Any dependencies listed in `pyproject.toml` or `poetry.lock`

Install dependencies using Poetry:

```bash
poetry install
```

---

For more details, see the source code in each module.

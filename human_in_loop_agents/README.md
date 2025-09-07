# Human-in-the-Loop Agents

This folder contains implementations of agents that incorporate human feedback, manual intervention, and decision-making into automated workflows. These agents are designed for scenarios where human judgment, approval, or guidance is essential for safe and effective operation.

## Overview

Human-in-the-loop agents combine automated reasoning with manual pauses, command classes, and time-travel concepts to allow users to interact, review, and steer the agent's actions.

### Main Components

- **Command Class** (`command_class.py`):
  - Defines command structures and logic for agent actions that can be triggered or modified by a human.

- **Manual Pause Agent** (`human_in_loop_manual_pause.py`):
  - Implements an agent that pauses at key decision points, waiting for human input before proceeding.

- **Multiturn Conversation Agent** (`multiturn_conversation_agent.py`):
  - Supports multi-turn dialogues with human feedback and intervention.

- **Resume Flow Operation** (`resume_flow_operation.py`):
  - Allows agents to resume operations after human review or approval.

- **Time Travel Concept** (`time_travel_concept.py`):
  - Explores agent state management and rollback for safe experimentation and human correction.

## How It Works

1. The agent performs automated reasoning and actions.
2. At predefined points, the agent pauses and requests human feedback or approval.
3. The human can review, modify, or approve the agent's next steps.
4. The agent resumes operation based on human input, ensuring safety and alignment with user goals.

## Example Usage

Run any of the scripts to see human-in-the-loop logic in action:

```bash
python3 human_in_loop_agents/human_in_loop_manual_pause.py
```

## Extensibility

- Add new human intervention points or feedback mechanisms.
- Extend command classes for more complex agent actions.

## Requirements

- Python 3.10+
- Any dependencies listed in `pyproject.toml` or `poetry.lock`

Install dependencies using Poetry:

```bash
poetry install
```

---
For more details, see the source code in each module.

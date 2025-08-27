from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model
from math_agent import math_agent
from research_agent import research_agent

"""
Creating a supervisor agnet using create_supervisor method
"""
supervisor = create_supervisor(
    model=init_chat_model("openai:gpt-4o"),
    agents=[research_agent, math_agent],
    prompt=(
        "You are a supervisor managing two agents:\n"
        "- a research agent. Assign research-related tasks to this agent\n"
        "- a math agent. Assign math-related tasks to this agent\n"
        "Assign work to one agent at a time, do not call agents in parallel.\n"
        "Do not do any work yourself."
    ),
    add_handoff_back_messages=True,
    output_mode="full_history",
).compile()

## Code to visualize agent structure graph

# from IPython.display import display, Image
# display(Image(supervisor.get_graph().draw_mermaid_png()))


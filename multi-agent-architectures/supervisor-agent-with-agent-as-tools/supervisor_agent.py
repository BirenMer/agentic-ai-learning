# langgraph_supervisor.py
from typing import List
from langchain_core.tools import BaseTool
from langgraph.prebuilt import create_react_agent
from langchain_core.language_models.chat_models import BaseChatModel

def create_supervisor(
    model: BaseChatModel,
    tools: List[BaseTool],
    prompt: str,
    add_handoff_back_messages: bool = True,
    output_mode: str = "full_history"
):
    """
    Create a supervisor agent that manages other agents as tools.
    
    Args:
        model: The language model to use for the supervisor
        tools: List of agent tools that the supervisor can use
        prompt: System prompt for the supervisor
        add_handoff_back_messages: Whether to add handoff messages
        output_mode: How to return the conversation history
    """
    
    # Create the supervisor using create_react_agent
    supervisor_graph = create_react_agent(
        model=model,
        tools=tools,
        prompt=prompt
    )
    
    return supervisor_graph

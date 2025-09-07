from typing import List

from langchain_core.messages import BaseMessage, ToolMessage, AIMessage
from langgraph.graph import END, MessageGraph

from chains import revisor_chain, first_responder_chain
from execution_tools import execute_tools

graph = MessageGraph()
MAX_ITERATIONS = 2

graph.add_node("draft", first_responder_chain)
graph.add_node("execute_tools", execute_tools)
graph.add_node("revisor", revisor_chain)


graph.add_edge("draft", "execute_tools")
graph.add_edge("execute_tools", "revisor")

def event_loop(state: List[BaseMessage]) -> str:
    count_tool_visits = sum(isinstance(item, ToolMessage) for item in state)
    num_iterations = count_tool_visits

    if num_iterations > MAX_ITERATIONS:
        return END

    # Check if the last message is an AI message with tool calls
    if (state and 
        isinstance(state[-1], AIMessage) and 
        getattr(state[-1], 'tool_calls', None)):
        return "execute_tools"

    return END

graph.add_conditional_edges("revisor", event_loop)
graph.set_entry_point("draft")

app = graph.compile()

## Visualize the graph
# print(app.get_graph().draw_mermaid())

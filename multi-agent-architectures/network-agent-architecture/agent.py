from langgraph.graph import StateGraph, START
from nodes import research_node,chart_node
from langgraph.graph import MessagesState

graph = StateGraph(MessagesState)
graph.add_node("researcher", research_node)
graph.add_node("chart_generator", chart_node)

graph.add_edge(START, "researcher")
app = graph.compile()


## Code to see the graph for agent structure
# from IPython.display import Image, display

# try:
#     display(Image(graph.get_graph().draw_mermaid_png()))
# except Exception:
#     # This requires some extra dependencies and is optional
#     pass
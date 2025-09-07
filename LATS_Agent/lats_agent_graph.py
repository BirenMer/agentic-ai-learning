from typing import Literal

from langgraph.graph import END, StateGraph, START
from tree_state import TreeState
from generate_initial_response import generate_initial_response
from candidate_generator import expand


def should_loop(state: TreeState):
    """Determine whether to continue the tree search."""
    root = state["root"]
    if root.is_solved:
        return END
    if root.height > 5:
        return END
    return "expand"


builder = StateGraph(TreeState)
builder.add_node("start", generate_initial_response)
builder.add_node("expand", expand)
builder.add_edge(START, "start")


builder.add_conditional_edges(
    "start",
    # Either expand/rollout or finish
    should_loop,
    ["expand", END],
)
builder.add_conditional_edges(
    "expand",
    # Either continue to rollout or finish
    should_loop,
    ["expand", END],
)

graph = builder.compile()

# Code to visualize the graph
# from IPython.display import Image
# Image(graph.get_graph().draw_mermaid_png())
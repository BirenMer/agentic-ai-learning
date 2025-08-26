"""
In this file we explore the command class in langgraph and see it in action 
No LLM needed
"""

from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from typing import TypedDict

class State(TypedDict):
    text: str

def node_a(state: State): 
    print("Node A")
    return Command(
        ## Where to go in the loop
        goto="node_b", 
        ## updating the state (Here a simple string)
        update={
            "text": state["text"] + "a"
        }
    )

def node_b(state: State): 
    print("Node B")
    return Command(
        goto="node_c", 
        update={
            "text": state["text"] + "b"
        }
    )


def node_c(state: State): 
    print("Node C")
    return Command(
        goto=END, 
        update={
            "text": state["text"] + "c"
        }
    )

graph = StateGraph(State)

graph.add_node("node_a", node_a)
graph.add_node("node_b", node_b)
graph.add_node("node_c", node_c)

graph.set_entry_point("node_a")


app = graph.compile()

response = app.invoke({
    "text": ""
})

print(f"response {response}")
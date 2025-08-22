from typing import Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import MessageGraph, END
from chains import generation_chain, reflection_chain

load_dotenv()

REFLECT = "reflect"
GENERATE = "generate"

def generate_node(state: Sequence[BaseMessage]):
    # returns an AIMessage
    print("\n\n Etenred Generation Node")
    return generation_chain.invoke({"messages": state})

def reflect_node(state: Sequence[BaseMessage]):
    # returns a HumanMessage so the next LLM call treats it as user feedback
    response = reflection_chain.invoke({"messages": state})
    print("\n\n Etenred Reflection Node")

    return HumanMessage(content=response.content)

def should_continue(state: Sequence[BaseMessage]):
    # stop after a few total messages (tune this)
    return "end" if len(state) > 6 else "generate"

graph = MessageGraph()
graph.add_node(GENERATE, generate_node)
graph.add_node(REFLECT, reflect_node)

graph.set_entry_point(GENERATE)

# ✅ this was missing — we need to actually go to REFLECT
graph.add_edge(GENERATE, REFLECT)

# After REFLECT, decide to loop back to GENERATE or END
graph.add_conditional_edges(
    REFLECT,
    should_continue,
    {
        "generate": GENERATE,
        "end": END,
    },
)

app = graph.compile()
print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()


response = app.invoke(HumanMessage(content="AI agents taking over content creation"))
print(f"\n\nFinal response: {response}\n")
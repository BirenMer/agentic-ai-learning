from langgraph.graph import StateGraph, START, END, add_messages
from typing import TypedDict, Annotated, List
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_community.tools import TavilySearchResults
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()
"""We will explore the concept of time travel using inturrept method.
We will be asked which tool to use before llm calls the tool"""

memory = MemorySaver()

search_tool = TavilySearchResults(max_results=2)
tools = [search_tool]

llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools=tools)

class BasicState(TypedDict): 
    messages: Annotated[List, add_messages]

def model(state: BasicState): 
    return {
        "messages": [llm_with_tools.invoke(state["messages"])]
    }

def tools_router(state: BasicState): 
    last_message = state["messages"][-1]
    if(hasattr(last_message, "tool_calls") and 
    len(last_message.tool_calls) > 0):
        return "tools"
    else: 
        return END


graph = StateGraph(BasicState)
graph.add_node(model, "model")
graph.add_node("tools", ToolNode(tools=tools))

graph.set_entry_point("model")
graph.add_conditional_edges("model", tools_router)

graph.add_edge("tools", "model")

app = graph.compile(checkpointer=memory,
                    ## Adding a inturrupt step 
                    interrupt_before=["tools"])

## To visualize the graph
# from IPython.display import Image, display
# display(Image(app.get_graph().draw_mermaid_png()))
config = {"configurable": {
    "thread_id": 1
}}

events = app.stream({
    "messages": [HumanMessage(content="What is the current weather in Ahmedabad, Gujarat, India?")]
}, config=config, 
## 
stream_mode="values")

for event in events:
    event["messages"][-1].pretty_print()

snapshot = app.get_state(config=config)
print(snapshot.next)

events = app.stream(None, config, stream_mode="values")
for event in events:
    event["messages"][-1].pretty_print()
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage
from langgraph.graph import add_messages, StateGraph, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

"""
Human in loop agent for content generation, using the manual input command and decision nodes
in_memory_checkpointer: To reflect on the agent's decision as well.
"""
class State(TypedDict): 
    messages: Annotated[list, add_messages]

## Defing model
llm = ChatOpenAI(model="gpt-4o")

#node names
GENERATE_POST = "generate_post"
GET_REVIEW_DECISION = "get_review_decision"
POST = "post"
COLLECT_FEEDBACK = "collect_feedback"

#Generate post node
def generate_post(state: State): 
    return {
        "messages": [llm.invoke(state["messages"])]
    }


## Human in loop deciding node
def get_review_decision(state: State):  
    post_content = state["messages"][-1].content 
    
    print("\n📢 Current LinkedIn Post:\n")
    print(post_content)
    print("\n")

    decision = input("Post to LinkedIn? (yes/no): ")

    if decision.lower() == "yes":
        return POST
    else:
        return COLLECT_FEEDBACK

## Final post retriver 
def post(state: State):  
    final_post = state["messages"][-1].content  
    print("\n📢 Final LinkedIn Post:\n")
    print(final_post)
    print("\n✅ Post has been approved and is now live on LinkedIn!")

#Feedback collector node
def collect_feedback(state: State):  
    feedback = input("How can I improve this post?")
    return {
        "messages": [HumanMessage(content=feedback)],
    }

## Graph init
graph = StateGraph(State)

#Adding nodes
graph.add_node(GENERATE_POST, generate_post)
graph.add_node(GET_REVIEW_DECISION, get_review_decision)
graph.add_node(COLLECT_FEEDBACK, collect_feedback)
graph.add_node(POST, post)

## Adding edges 
graph.set_entry_point(GENERATE_POST)

graph.add_conditional_edges(GENERATE_POST, get_review_decision)
graph.add_edge(POST, END)
graph.add_edge(COLLECT_FEEDBACK, GENERATE_POST)

## Creating memory checkpointer
in_memory_checkpointer=MemorySaver()

## Creating memory checkpoint
config={"configurable":{
    "thread_id":1
}}

#Compiling the graph
app = graph.compile(checkpointer=in_memory_checkpointer)

response = app.invoke({
    "messages": [HumanMessage(content="Write me a LinkedIn post on AI Agents taking over content creation")],
    
},config=config)

print(response)

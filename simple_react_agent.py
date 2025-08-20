"""
Agent-3
ReAct Agent
Objectives:
    1. Learn how to create Tools in LangGraph
    2. How to create a ReAct Graph
    3. Work with different types of Messages such as ToolMessages
    4. Test out robustness of our graph

Main Goal: Create a robust ReAct Agent!
"""
from typing import Annotated,Sequence,TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage #The foundational class for all message types in Langgraph
from langchain_core.messages import ToolMessage # Passes data back to LLM after it calls a tool such as the content and the tool_call_id
from langchain_core.messages import SystemMessage # Message for providing instructions to LLM
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool #Used to declare a function as a tool
from langgraph.graph.message import add_messages # It is a reducer function
from langgraph.graph import StateGraph,END
from langgraph.prebuilt import ToolNode

## What is annotated ?
email=Annotated[str,"This should be printed in meta data"]
print(email.__metadata__)

# Sequence - To automatically handle the state updates for sequences such as by adding new messages to a chat history 
## What is add_messages:
# It is a Reducer function : A function that takes two inputs: a current state and an action, and returns a new state
# In other words a Rule that controls how updates from nodes are combined with the existing state.
# Tells us how to merge new data into current state.
# Without a reducer, updates would have replaced the existing value enteirly! 

## Creating React Example
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage],add_messages]

## Defining a tool
@tool
def add(a:int,b:int):
    """This is a addition function that adds two numbers"""
    return a+b

tools=[add] #can have multiple tools as well

model=ChatOpenAI(model='gpt-4o').bind_tools(tools) #Binding the tool we created

#Defining mdoel call / agent function
def model_call(state:AgentState)->AgentState:
    system_prompt=SystemMessage(content="You are my AI assistant, Please answer my query to the best of your ability.")
    response = model.invoke( [system_prompt] + state["messages"])
    return {"messages":[response]} #this will update the state messages


## Defining the contdition edge function
def should_continue(state:AgentState):
    
    messages=state['messages']
    last_message=messages[-1] #retiving the last message 

    if not last_message.tool_calls: #checking if any tools are needed to be retrived
        return "end" # no
    else:
        return "continue" # yes
    
## Defining graph 
graph=StateGraph(AgentState)
##Deifning a tool node
tool_node=ToolNode(tools)

#deifining other nodes
graph.add_node("agent",model_call)
graph.add_node("tools",tool_node)

#setting entry points
graph.set_entry_point("agent")

#addign condition edge
graph.add_conditional_edges(
    "agent", #main node
    should_continue, #condition functuion
    #routing path to nodes
    {
        "continue":"tools",
        "end":END
    }
)
#creating a loop 
graph.add_edge("tools","agent")

#finally compiling the graph
app=graph.compile()

## Function to print messages in a better way
def print_stream(stream):
    for s in stream:
        print(s)
        message=s['messages'][-1]
        if isinstance(message,tuple):
            print(message)
        else:
            message.pretty_print()

inputs={"messages":[("user","add 31+25. and add 3+8")]}
print_stream(app.stream(inputs,stream_mode="values"))

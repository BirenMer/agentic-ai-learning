"""
Agent 2
    Objectives:
    Use different message types - HumanMessage and AIMessage
    Maintain a full conversation history using both message types
    Use GPT-40 model using LangChain's ChatOpenAI
    Create a sophisticated conversation loop
    Main Goal: Create a form of memory for our Agent
"""
import os 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,AIMessage
from langgraph.graph import StateGraph,START,END
from typing import TypedDict,List,Union
load_dotenv()
class AgentState(TypedDict):
    messages:List[Union[HumanMessage,AIMessage]] #This allows us to store either human message or ai message.

llm=ChatOpenAI(model='gpt-4o')
def process(state:AgentState) -> AgentState:
    """This node will solve the request you input"""
    response=llm.invoke(state["messages"])
    state['messages'].append(AIMessage(content=response.content))
    print(f"\n AI {response.content}")
    print(f"Current State: {state['messages']}")
    return state

graph=StateGraph(AgentState)
graph.add_node("process",process)
graph.add_edge(START,"process")
graph.add_edge("process",END)

agent=graph.compile()

#Limitation:
# 1. Memory lasts only till the run is active
# 2. Too much context is send with the chat to the llm making this expensive in time and cost
 
converstation_history=[]

user_input=input("Enter: ")
while user_input!="exit":
    converstation_history.append(HumanMessage(content=user_input))
    result=agent.invoke({"messages":converstation_history})
    user_input=input("Enter: ")

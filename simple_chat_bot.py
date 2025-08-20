"""
Agent 1 : Simple Chat Bot
Objectives:
        Define state structure with a list of HumanMessage objects.
        Initialize a GPT-4o model using LangChain's ChatOpenAI
        Sending and handling different types of messages
        Building and compiling the graph of the Agent
        Main Goal: How to integrate LLMs in our Graphs
"""

from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START,END
from dotenv import load_dotenv
import os

load_dotenv()
class AgentState(TypedDict):
    message:List[HumanMessage]

llm=ChatOpenAI(model="gpt-4o")

#Defining process
def process(state:AgentState)-> AgentState:
    response=llm.invoke(state["message"])
    print(f"{response.content}")
    return state

#Creating graph strcutre
graph=StateGraph(AgentState)
graph.add_node("process",process)
graph.add_edge(START,"process")
graph.add_edge("process",END)

#Compiling graph
agent=graph.compile()

#Creating a iteration loop for chatbot
user_input=input("Enter: ")
while user_input!="exit":
    agent.invoke({"message":[HumanMessage(content=user_input)]})
    user_input=input("Enter: ")

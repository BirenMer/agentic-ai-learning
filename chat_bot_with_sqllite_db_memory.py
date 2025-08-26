from typing import Annotated,Sequence,TypedDict
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages 
from langgraph.graph import StateGraph,END,START
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
load_dotenv()

"""
Goal : Create a chat bot and provide it with a sqllite memory and test if it is working or not.
"""

## Connecting / Creating the DB
sqllite_conn=sqlite3.connect("checkpoint.sqlite")

llm=ChatOpenAI(model='gpt-4o',temperature=0)

class AgentState(TypedDict):   
    messages: Annotated[list,add_messages]

def chatbot(state:AgentState) -> AgentState:
    return {"messages":llm.invoke(state["messages"])}
      
graph=StateGraph(AgentState)
graph.add_node("chatbot",chatbot)
graph.add_edge(START,"chatbot")
graph.add_edge("chatbot",END)

config={"configurable":{
    "thread_id":1
}}

sqlite_checkpointer=SqliteSaver(sqllite_conn)
app=graph.compile(checkpointer=sqlite_checkpointer)

#To check the graph strcutre
# from IPython.display import Image,display
# display(Image(app.get_graph().draw_mermaid_png()))

while True:
    user_input=input("User: ")
    if user_input in ["exit", "quit", "break"]:
        break
    else:
        # print(f"User: {user_input}")
        result=app.invoke(
           { "messages":[HumanMessage(content=user_input)]},
           config=config
        )

        print(f"AI: {result['messages'][-1].content}")
    # print(result)
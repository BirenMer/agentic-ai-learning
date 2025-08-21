"""
Agent 4
Drafter:
    Our company is not working efficiently! We spend way too much time drafting documents and this needs to be fixed! ⏱️
    For the company, you need to create an AI Agentic System that can speed up drafting documents, emails, etc. 
    The AI Agentic System should have Human-AI Collaboration meaning the Human should be able to able to provide continuous feedback and the AI Agent should stop when the Human is happy with the draft. 
    The system should also be fast and be able to save the drafts.
    The text has been successfully extracted and converted to plain text format. If you need this saved as a .txt file, I can create that for you as well.
"""
from typing import Annotated,Sequence,TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage 
from langchain_core.messages import ToolMessage 
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage 
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool 
from langgraph.graph.message import add_messages 
from langgraph.graph import StateGraph,END
from langgraph.prebuilt import ToolNode

load_dotenv()

## Global Variable to store document content
document_content=""

class AgentState(TypedDict):
    messages:Annotated[Sequence[BaseMessage],add_messages]

@tool
def update(content:str)->str:
    """Updates the document with the provided content"""
    global document_content
    document_content=content
    return f"Document Content has been updated successfully! The current content is \n{document_content}"

@tool 
def save(filename:str)->str:
    """Save the current document to a text file and finish the process"""
    global document_content
    if not filename.endswith(".txt"):
        filename=f"{filename}.txt"
    try:
        with open(filename,'w') as file:
            file.write(document_content)
        print(f"Document has been save to {filename}")
        return f"Document has been saved successfully to {filename}"
    
    except Exception as e:
        print(e)
        return f"Error saving the document {e}"
    
tools=[update,save]
model=ChatOpenAI(model='gpt-4o').bind_tools(tools)

def agent(state:AgentState):
    system_prompt=SystemMessage(content=f"""You are Drafter, a helpful writing assistant. You are going to help the user update and modify documents.
                                        - If the user wants to update or modify content, use the 'update' tool with the complete updated content.
                                        - If the user wants to save and finish, you need to use the 'save' tool.
                                        - Make sure to always show the current document state after modifications.

                                        The current document content is: {document_content}
                                        """)
    
    if not state['messages']:
    
        user_input="I'm ready to help you update a document. What would you like to create ?"
        user_message=HumanMessage(content=user_input)
    
    else:
        user_input=input("\n What would you like to do with the document?")
        print(f"\n User: {user_input}")
        user_message=HumanMessage(content=user_input)
        
    all_messages=[system_prompt]+list(state['messages'])+[user_message]
    
    response=model.invoke(all_messages)

    if hasattr(response,"tool_calls") and response.tool_calls:
        print(f"Using Tool: {[tc['name'] for tc in response.tool_calls]}")

    return {'messages':list(state['messages'])+[user_message,response]}

def should_continue(state:AgentState)->str:
    """Determin if we should continue or end the conversation"""
    
    message=state["messages"]
    
    if not message:
        return "continue"
    
    ## The bleow code looks for the most recent message...
    for message in reversed(message):
        #..... and checks if this is a Tool Message resulting from save
        #Logic being we continue the loop if we are updating the doc and if we save it we end the flow
        if(isinstance(message,ToolMessage) and 
           "saved" in str(message.content).lower() and
           "document" in str(message.content).lower()):
            return "end"
    return "continue"
        
def print_message(messages):
        """Function to print the messages properly"""
        if not messages:
            return
        for message in messages[-3:]:
              if isinstance(message,ToolMessage):
                    print(f"\n Tool Result: {message.content}")

graph=StateGraph(AgentState)
graph.add_node("agent",agent)
graph.add_node("tools",ToolNode(tools))

graph.set_entry_point("agent")
graph.add_edge("agent","tools")
graph.add_conditional_edges(
    "tools",
    should_continue,
    {
        "continue":"agent",
        "end":END
    }
)

app=graph.compile()

def run_drafter_agent():
    print("\n Drafter Agent Started")
    state = {"messages":[]}
    for step in app.stream(state,stream_mode="values"):
        if "messages" in step:
            print_message(step["messages"])
    print("\n Drafter Agent Finish")

if __name__=='__main__':
    run_drafter_agent()
from typing import Annotated,Sequence,TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage 
from langchain_core.messages import ToolMessage 
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage 
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool 
# from langgraph.graph.message import add_messages 
from langgraph.graph import StateGraph,END
from langgraph.prebuilt import ToolNode
from operator import add as add_messages
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.tools import tool
import os

#setting the temp to zero to reduce hallucinations
llm=ChatOpenAI(model='gpt-4o',temperature=0)
## Setting up embedding model
## Making sure that the model is compatible with our llm i.e. both models are of open ai
embeddings=OpenAIEmbeddings(
    model="text-embedding-3-small"
)
pdf_path="Stock_Market_Performance_2024.pdf"
if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"PDF file not found: {pdf_path}")
pdf_loader=PyPDFLoader(pdf_path)

#Loading the pdf
try: 
    pages=pdf_loader.load()
    print(f"PDF has been loaded and has {len(pages)} pages.")
except Exception as e:
    print(f"Error Loading PDF: {e}")

text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

pages_split=text_splitter.split_documents(pages)
persist_directory="./RAG_agent_data"
collection_name="us_stock_market"

#Creating collection if it does not exits
if os.path.exists(persist_directory):
    os.makedirs(persist_directory)

try:
    vectorstore=Chroma.from_documents(
        documents=pages_split,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name
    )
    print(f"Created ChromaDB vectore store")
except Exception as e:
    print(f"Error setting up ChromaDB: {str(e)}")


## Creating a retriever
retriever=vectorstore.as_retriever(
    seach_type="similarity",
    search_kwargs={'k':5} #K is the amount of chunks to return
)

@tool
def retriever_tool(query:str)->str:
    """
    This tool searchs and returns the information from the stock market performance 2024 doc
    """
    docs=retriever.invoke(query)
    
    if not docs:
        return "I found no relvaent infomation in the stock market performance 2024 doc"
    
    results=[]
    for i,doc in enumerate(docs):
        results.append(f"Document {i+1}:\n{doc.page_content}")

    return "\n\n".join(results)

tools=[retriever_tool]

llm=llm.bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage],add_messages]

def should_continue(state:  AgentState):
    """Check if the last message contains tool calls"""
    result=state['messages'][-1]
    return hasattr(result,'tool_calls') and len(result.tool_calls) > 0

system_prompt=SystemMessage(content="""
You are an intelligent AI assistant who answers questions about Stock Market Performance in 2024 based on the PDF document loaded into your knowledge base.
Use the retriever tool available to answer questions about the stock market performance data. You can make multiple calls if needed.
If you need to look up some information before asking a follow up question, you are allowed to do that!
Please always cite the specific parts of the documents you use in your answers.
""")

# Creating a dict of our tools
tools_dict={our_tool.name: our_tool for our_tool in tools}

## Agent for llm call
def call_llm(state:AgentState):
    """Function to call the LLM with the current state"""
    messages=list(state['messages'])
    messages=[system_prompt]+messages
    messages=llm.invoke(messages)
    return {'messages':[messages]}

# Retriever Agent
def take_action(state: AgentState) -> AgentState:
    """Execute tool calls from the LLM's response."""

    tool_calls = state['messages'][-1].tool_calls
    results = []
    for t in tool_calls:
        print(f"Calling Tool: {t['name']} with query: {t['args'].get('query', 'No query provided')}")
        
        if not t['name'] in tools_dict: # Checks if a valid tool is present
            print(f"\nTool: {t['name']} does not exist.")
            result = "Incorrect Tool Name, Please Retry and Select tool from List of Available tools."
        
        else:
            result = tools_dict[t['name']].invoke(t['args'].get('query', ''))
            print(f"Result length: {len(str(result))}")
            

        # Appends the Tool Message
        results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))

    print("Tools Execution Complete. Back to the model!")
    return {'messages': results}
#Defining Agent Structure
graph=StateGraph(AgentState)

#deining nodes
graph.add_node("llm_agent",call_llm)
graph.add_node("retriever_agent",take_action)

#Defining edges
graph.set_entry_point("llm_agent")
graph.add_conditional_edges(
    "llm_agent",
    should_continue,
    {
        True:"retriever_agent",
        False:END
    }
)
graph.add_edge("retriever_agent","llm_agent")

rag_agent=graph.compile()

def running_agent():
    print("\n=== RAG AGENT===")
    
    while True:
        user_input = input("\nWhat is your question: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        messages = [HumanMessage(content=user_input)] # converts back to a HumanMessage type

        result = rag_agent.invoke({"messages": messages})
        
        print("\n=== ANSWER ===")
        print(result['messages'][-1].content)

if __name__=='__main__':
    running_agent()
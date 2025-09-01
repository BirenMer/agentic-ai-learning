# research_agent.py
from langgraph.prebuilt import create_react_agent
from typing import Annotated
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from tools import web_search
from langgraph.prebuilt import InjectedState

load_dotenv()

def create_research_agent():
    """Create a research agent that can be used as a tool by the supervisor"""
    
    system_message = """
    You are a research agent specialized in finding and analyzing information from the web.
    
    INSTRUCTIONS:
    - Use the web search tool to find relevant information
    - Provide comprehensive and accurate research results
    - Focus on factual information and cite sources when possible
    - If you cannot find information, clearly state this
    - Do NOT attempt to solve mathematical problems - that's for the math agent
    """
    
    # Create the research agent using create_react_agent
    research_graph = create_react_agent(
        model=ChatOpenAI(model="gpt-4o"),
        tools=[web_search],
    )
    
    def research_agent_tool(query: str) -> str:
        """
        Research agent that searches for information on the web.
        Use this for any research-related tasks, fact-finding, or information gathering.
        """
        try:
            # Invoke the research agent with the query
            result = research_graph.invoke({"messages": [("system",system_message),("human", query)]})
            
            # Extract the final response from the agent
            final_message = result["messages"][-1]
            return final_message.content
        except Exception as e:
            return f"Error in research agent: {str(e)}"
    
    return research_agent_tool
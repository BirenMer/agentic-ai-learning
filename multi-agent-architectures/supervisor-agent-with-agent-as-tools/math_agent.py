# math_agent.py
from langgraph.prebuilt import create_react_agent
from typing import Annotated
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from tools import calculator_tool
from langgraph.prebuilt import InjectedState

load_dotenv()

def create_math_agent():
    """Create a math agent that can be used as a tool by the supervisor"""
    
    system_message = """
    You are a math agent specialized in solving mathematical problems and calculations.
    
    INSTRUCTIONS:
    - Use the calculator tool for mathematical computations
    - Break down complex problems into steps
    - Provide clear explanations of your mathematical reasoning
    - Handle various types of math: arithmetic, algebra, calculus concepts, etc.
    - If you cannot solve a problem, explain why
    - Do NOT attempt to do research - that's for the research agent
    """
    
    # Create the math agent using create_react_agent
    math_graph = create_react_agent(
        model=ChatOpenAI(model="gpt-4o"),
        tools=[calculator_tool],
    )
    
    def math_agent_tool(problem: str) -> str:
        """
        Math agent that solves mathematical problems and performs calculations.
        Use this for any math-related tasks, calculations, or problem-solving.
        """
        try:
            # Invoke the math agent with the problem
            result = math_graph.invoke({"messages": [("system",system_message),("human", problem)]})
            
            # Extract the final response from the agent
            final_message = result["messages"][-1]
            return final_message.content
        except Exception as e:
            return f"Error in math agent: {str(e)}"
    
    return math_agent_tool

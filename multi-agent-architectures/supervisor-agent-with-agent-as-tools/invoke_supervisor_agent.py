#main.py - Complete implementation
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from research_agent import create_research_agent
from math_agent import create_math_agent
from supervisor_agent import create_supervisor

# from langgraph_supervisor import create_supervisor

load_dotenv()

def main():
    # Create agent tools
    research_agent_tool = create_research_agent()
    math_agent_tool = create_math_agent()
    
    # Convert functions to LangChain tools
    @tool
    def research_agent(query: str) -> str:
        """Research agent for finding information and conducting research tasks."""
        return research_agent_tool(query)
    
    @tool  
    def math_agent(problem: str) -> str:
        """Math agent for solving mathematical problems and calculations."""
        return math_agent_tool(problem)
    
    # Create supervisor
    supervisor = create_supervisor(
        model=ChatOpenAI(model="gpt-4o"),
        tools=[research_agent, math_agent],
        prompt=(
            "You are a supervisor managing two agents:\n"
            "- a research agent: Assign research-related tasks to this agent\n"
            "- a math agent: Assign math-related tasks to this agent\n"
            "Assign work to one agent at a time, do not call agents in parallel.\n"
            "Do not do any work yourself. Always delegate to the appropriate agent.\n"
            "After receiving results from an agent, provide a clear summary to the user."
        ),
        add_handoff_back_messages=True,
        output_mode="full_history",
    )
    
    return supervisor

# Example usage
if __name__ == "__main__":
    # Initialize the supervisor
    supervisor = main()
    
    # Test the supervisor with different types of queries
    test_queries = [
        "What is the current price of Bitcoin?",
        "Calculate the area of a circle with radius 5",
        "Research the latest developments in AI safety",
        "Solve this equation: 2x + 5 = 15"
    ]
    
    for query in test_queries:
        print(f"\n--- Query: {query} ---")
        try:
            result = supervisor.invoke({"messages": [("human", query)]})
            final_response = result["messages"][-1].content
            print(f"Response: {final_response}")
        except Exception as e:
            print(f"Error: {e}")

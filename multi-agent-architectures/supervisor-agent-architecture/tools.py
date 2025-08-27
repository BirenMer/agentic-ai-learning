from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

web_search = TavilySearch(max_results=3)

@tool
def add(a: float, b: float):
    """Add two numbers."""
    return a + b

@tool
def multiply(a: float, b: float):
    """Multiply two numbers."""
    return a * b

@tool
def divide(a: float, b: float):
    """Divide two numbers."""
    return a / b

## Test the Tool
# web_search_results = web_search.invoke("who is the mayor of NYC?")
# print(web_search_results["results"][0]["content"])
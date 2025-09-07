from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langgraph.prebuilt import ToolNode
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()

tavily_tool = TavilySearch(max_results=5)
tools = [tavily_tool]
tool_node = ToolNode(tools=tools)
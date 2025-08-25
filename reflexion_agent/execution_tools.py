import json
from typing import List
from langchain_core.messages import AIMessage, BaseMessage, ToolMessage, HumanMessage
from langchain_community.tools import TavilySearchResults
from dotenv import load_dotenv
load_dotenv()
# Create the Tavily search tool
tavily_tool = TavilySearchResults(max_results=5)

# Function to execute search queries from AnswerQuestion / ReviseAnswer tool calls
def execute_tools(state: List[BaseMessage]) -> List[BaseMessage]:
    if not state:
        return state

    last_message = state[-1]

    # Only process if last message is an AI message with tool calls
    if not isinstance(last_message, AIMessage) or not getattr(last_message, "tool_calls", None):
        return state

    tool_messages: List[BaseMessage] = []

    for tool_call in last_message.tool_calls:
        if tool_call["name"] in ["AnswerQuestion", "ReviseAnswer"]:
            call_id = tool_call["id"]
            search_queries = tool_call["args"].get("search_queries", [])

            query_results = {}
            for query in search_queries:
                try:
                    result = tavily_tool.invoke({"query": query})
                    query_results[query] = result
                except Exception as e:
                    query_results[query] = {"error": str(e)}

            tool_messages.append(
                ToolMessage(
                    content=json.dumps(query_results, ensure_ascii=False, indent=2),
                    tool_call_id=call_id,
                )
            )

    # Return original state + new tool messages
    return state + tool_messages


# Example usage
test_state = [
    HumanMessage(content="Write about how small business can leverage AI to grow"),
    AIMessage(
        content="",
        tool_calls=[
            {
                "name": "AnswerQuestion",
                "args": {
                    "answer": "",
                    "search_queries": [
                        "AI tools for small business",
                        "AI in small business marketing",
                        "AI automation for small business",
                    ],
                    "reflection": {"missing": "", "superfluous": ""},
                },
                "id": "call_KpYHichFFEmLitHFvFhKy1Ra",
            }
        ],
    ),
]

# Execute the tools
results = execute_tools(test_state)

print("Raw results:", results[-1].content)
parsed_content = json.loads(results[-1].content)
print("Parsed content:", parsed_content)

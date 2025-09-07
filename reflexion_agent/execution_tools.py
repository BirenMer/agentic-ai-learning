import json
from typing import List
from langchain_core.messages import AIMessage, BaseMessage, ToolMessage, HumanMessage
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
load_dotenv()

# Create the Tavily search tool
tavily_tool = TavilySearch(max_results=5)

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
        name = tool_call["name"]
        call_id = tool_call["id"]
        args = tool_call.get("args", {})

        if name in ["AnswerQuestion", "ReviseAnswer"]:
            search_queries = args.get("search_queries", [])
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

        else:
            # 👇 fallback: wrap unknown schema/object safely
            try:
                safe_content = (
                    args if isinstance(args, str) else json.dumps(args, ensure_ascii=False, indent=2)
                )
            except Exception:
                safe_content = str(args)

            tool_messages.append(
                ToolMessage(
                    content=safe_content,
                    tool_call_id=call_id,
                )
            )

    return state + tool_messages

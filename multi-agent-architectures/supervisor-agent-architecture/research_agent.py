from langgraph.prebuilt import create_react_agent
from tools import web_search
from dotenv import load_dotenv
load_dotenv()
"""Research agent: ReactAct agent using travelly search tool for seaching the web"""
## Defining a research Agent
research_agent = create_react_agent(
    model="openai:gpt-4o",
    tools=[web_search],
    prompt=(
        "You are a research agent.\n\n"
        "INSTRUCTIONS:\n"
        "- Assist ONLY with research-related tasks, DO NOT do any math\n"
        "- After you're done with your tasks, respond to the supervisor directly\n"
        "- Respond ONLY with the results of your work, do NOT include ANY other text."
    ),
    name="research_agent",
)
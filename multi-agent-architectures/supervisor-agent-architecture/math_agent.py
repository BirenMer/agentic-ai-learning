from langgraph.prebuilt import create_react_agent
from tools import add,multiply,divide
from dotenv import load_dotenv

load_dotenv()
"""Math agent: ReactAct agent using add, multiply and divide python basic functions as tools"""
math_agent = create_react_agent(
    model="openai:gpt-4o",
    tools=[add, multiply, divide],
    prompt=(
        "You are a math agent.\n\n"
        "INSTRUCTIONS:\n"
        "- Assist ONLY with math-related tasks\n"
        "- After you're done with your tasks, respond to the supervisor directly\n"
        "- Respond ONLY with the results of your work, do NOT include ANY other text."
    ),
    name="math_agent",
)
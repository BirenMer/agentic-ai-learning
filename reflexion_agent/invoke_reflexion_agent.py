from reflexion_agent_graph import app
from langchain_core.messages import AIMessage

response = app.invoke(
    "Write about how small business can leverage AI to grow"
)

# Find the last AI message with tool calls
for message in reversed(response):
    if isinstance(message, AIMessage) and getattr(message, 'tool_calls', None):
        print(message.tool_calls[0]["args"]["answer"])
        break

print("Full response:", response)
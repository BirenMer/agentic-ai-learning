from supervisor_agent import supervisor
from print_utils import pretty_print_messages

"""Main file to run the supervisor agent with both math and research agent"""
final_history={}
for chunk in supervisor.stream(
    {
        "messages": [
            {
                "role": "user",
                "content": "Find India and Gujarat state GDP in 2024. what % of India's GDP was Gujarat state?",
            }
        ]
    },
):
    pretty_print_messages(chunk, last_message=True)

    ## Print Statement to visualize chunk messages
    # print("===========================")
    # print(chunk)
    # print("===========================")

    if "supervisor" in chunk:
        final_message_history = chunk["supervisor"]["messages"]
    else:
        continue
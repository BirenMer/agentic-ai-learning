from print_utils import pretty_print_message,pretty_print_messages

from research_agent import research_agent

"""File to test if the reseach agent works porperly"""


for chunk in research_agent.stream(
    {"messages": [{"role": "user", "content": "who is the mayor of NYC?"}]}
):
    pretty_print_messages(chunk)
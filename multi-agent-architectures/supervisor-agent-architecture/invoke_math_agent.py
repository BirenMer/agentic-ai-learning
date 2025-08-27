from print_utils import pretty_print_messages
from math_agent import math_agent

"""File to test if the math agent works porperly"""

for chunk in math_agent.stream(
    {"messages": [{"role": "user", "content": "what's (3 + 5) x 7"}]}
):
    pretty_print_messages(chunk)
from typing import Literal, TypedDict, Union,Callable,Any
from langchain_core.language_models.chat_models import BaseChatModel

from langgraph.graph import MessagesState, END
from langgraph.types import Command
from dotenv import load_dotenv

load_dotenv()

class State(MessagesState):
    next: str

## This function will help us in creating two things

def make_supervisor_node(llm: BaseChatModel, members: list[str]) -> Callable[[State], Command[Any]]:
    options = ["FINISH"] + members
    system_prompt = (
        "You are a supervisor tasked with managing a conversation between the"
        f" following workers: {members}. Given the following user request,"
        " respond with the worker to act next. Each worker will perform a"
        " task and respond with their results and status. When finished,"
        " respond with FINISH."
    )

    class Router(TypedDict):
        """Worker to route to next. If no workers needed, route to FINISH."""
        next: str  # Using str instead of Literal[*options] due to syntax limitations

    def supervisor_node(state: State) -> Command[Literal["__end__"]]:
        """An LLM-based router."""
        messages = [
            {"role": "system", "content": system_prompt},
        ] + state["messages"]
        response = llm.with_structured_output(Router).invoke(messages)
        goto = response["next"]
        
        # Runtime validation to ensure only valid options are used
        if goto not in options:
            raise ValueError(f"Invalid routing option: {goto}. Valid options: {options}")
            
        if goto == "FINISH":
            goto = END

        return Command(goto=goto, update={"next": goto})

    return supervisor_node
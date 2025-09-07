from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import datetime
from langchain_openai import ChatOpenAI
from schema import AnswerQuestion, ReviseAnswer
from langchain_openai.output_parsers.tools import PydanticToolsParser
from langchain_core.messages import HumanMessage, ToolMessage
from dotenv import load_dotenv
import json

load_dotenv()

def schema_to_tool_message(schema_obj, call_id="schema_output"):
    # Handle single schema object
    if hasattr(schema_obj, "dict"):
        return ToolMessage(
            content=json.dumps(schema_obj.dict(), indent=2, ensure_ascii=False),
            tool_call_id=call_id,
        )
    # Handle list of schema objects
    elif isinstance(schema_obj, list):
        return ToolMessage(
            content=json.dumps([obj.dict() for obj in schema_obj], indent=2, ensure_ascii=False),
            tool_call_id=call_id,
        )
    else:
        raise TypeError(f"Unexpected schema_obj type: {type(schema_obj)}")

# ---------------------------
# Prompts
# ---------------------------
actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """ 
            You are expert AI researcher.
            {messages}
            Current time: {time}

            1. {first_instruction}
            2. Reflect and critique your answer. Be severe to maximize improvement.
            3. After the reflection, **list 1-3 search queries separately** for researching improvements. 
               Do not include them inside the reflection.
            """,
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Answer the user's question above using the required format."),
    ]
).partial(time=lambda: datetime.datetime.now().isoformat())

first_responders_prompt_template = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word answer"
)

# ---------------------------
# LLM + Tool Binding
# ---------------------------
llm = ChatOpenAI(model="gpt-4o")

responder_llm = llm.bind_tools(
    [AnswerQuestion],
    tool_choice="AnswerQuestion"  # force the tool call
)

# ---------------------------
# Parsers
# ---------------------------
responder_parser = PydanticToolsParser(tools=[AnswerQuestion])

# ---------------------------
# Chains
# ---------------------------
first_responder_chain = (
    first_responders_prompt_template
    | responder_llm
)

revise_instructions = """Revise your previous answer using the new information.
    - Use the previous critique to add important information.
    - Include numerical citations in your revised answer (for verification).
    - Add a "References" section at the bottom (not part of word count).
        - [1] https://example.com
        - [2] https://example.com
    - Remove superfluous information and ensure < 250 words.
"""

revisor_llm = llm.bind_tools([ReviseAnswer], tool_choice="ReviseAnswer")
revisor_parser = PydanticToolsParser(tools=[ReviseAnswer])

revisor_chain = (
    actor_prompt_template.partial(first_instruction=revise_instructions)
    | revisor_llm
)

# ---------------------------
# Example Test
# ---------------------------
# if __name__ == "__main__":
#     response = first_responder_chain.invoke({
#         "messages": [HumanMessage(content="AI Agents taking over content creation")]
#     })
#     print("First Responder Output:", response)

#     revised = revisor_chain.invoke({
#         "messages": [HumanMessage(content="AI Agents taking over content creation")]
#     })
#     print("Revised Output:", revised)

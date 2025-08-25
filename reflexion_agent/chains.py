from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
import datetime
from langchain_openai import ChatOpenAI
from schema import AnswerQuestion,ReviseAnswer
from langchain_openai.output_parsers.tools import PydanticToolsParser
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
load_dotenv()
#Pydantic Parser
pydantic_parser=PydanticToolsParser(tools=[AnswerQuestion])

# Actor Agent Prompt
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
            3. After the reflection, **list 1-3 search queries separately** for researching improvements. Do not include them inside the reflection.
        """,
    ),
    MessagesPlaceholder(variable_name="messages"),
    ("system", "Answer the user's question above using the required format."),
]
# We are performaing a partial to pre populate the variable time
).partial(time=lambda:datetime.datetime.now().isoformat(),)

## We are using the actor prompt and filling the first instruction
first_responders_prompt_template=actor_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word answer")

## llm
llm=ChatOpenAI(model='gpt-4o')

responder_llm=llm.bind_tools(
    [AnswerQuestion],
    ## Since we have this only tool we will 
    # force the llm to call that tool
    tool_choice='AnswerQuestion'
    )

## First responder chain
first_responder_chain=first_responders_prompt_template | responder_llm | pydantic_parser

## Chain Test code
# response=first_reponder_chain.invoke({"messages":[HumanMessage(content="Write me a blog post on how small bussiness can leverage AI to grow")]})
# print(response)


# Revisor section

revise_instructions = """Revise your previous answer using the new information.
    - You should use the previous critique to add important information to your answer.
        - You MUST include numerical citations in your revised answer to ensure it can be verified.
        - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
            - [1] https://example.com
            - [2] https://example.com
    - You should use the previous critique to remove superfluous information from your answer and make SURE it is not more than 250 words.
"""

#binding tool for revisor agent
revisor_llm=llm.bind_tools(tools=[ReviseAnswer], tool_choice="ReviseAnswer")

revisor_chain = actor_prompt_template.partial(
    first_instruction=revise_instructions
) | revisor_llm

response = first_responder_chain.invoke({
    "messages": [HumanMessage("AI Agents taking over content creation")]
})

print(response)

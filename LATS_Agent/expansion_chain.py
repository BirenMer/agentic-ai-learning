# This generates N candidate values
# for a single input to sample actions from the environment
from langchain_core.prompt_values import ChatPromptValue
from langchain_core.runnables import RunnableConfig
from model import llm
from tools import tools
from inital_answer_chain import prompt_template
from langchain_core.runnables import RunnableLambda


def generate_candidates(messages: ChatPromptValue, config: RunnableConfig):
    n = config["configurable"].get("N", 5)
    bound_kwargs = llm.bind_tools(tools=tools).kwargs
    chat_result = llm.generate(
        [messages.to_messages()],
        n=n,
        callbacks=config["callbacks"],
        run_name="GenerateCandidates",
        **bound_kwargs,
    )
    return [gen.message for gen in chat_result.generations[0]]

generate_candidates_runnable = RunnableLambda(generate_candidates)
expansion_chain = prompt_template | generate_candidates_runnable

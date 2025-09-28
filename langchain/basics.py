from langchain_openai import ChatOpenAI

from langchain_core.prompts import (
            SystemMessagePromptTemplate, 
            HumanMessagePromptTemplate,
            AIMessagePromptTemplate,
            ChatPromptTemplate
)
from pydantic import BaseModel, Field

from dotenv import load_dotenv

load_dotenv()

"""
For this file our goal is to levarage Langchain and LLM's capabilities to :
1. Get title for the article in chain one.
2. Get a summary for the provided Article.
3. Get a reviewe for the provided Article.

"""

with open("langchain/data/article.txt", "r") as f:
    content = f.read()

llm=ChatOpenAI(model="gpt-4o",temperature=0.9)

# Defining the system prompt (how the AI should behave)
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are an AI assistant that helps in aritcle related task."
)

# The user prompt is provided by the user, in this case however the only dynamic
# input is the article
title_generator_user_prompt = HumanMessagePromptTemplate.from_template(
    """You are tasked with creating a name for a article.
    The article is here for you to examine: {article}
    
    The name should be based of the context of the article.
    Be creative, but make sure the names are clear, catchy,
    and relevant to the theme of the article.
    
    Only output the article name, no other explanation or
    text can be provided.""",
    input_variables=["article"]
)

##Testing what we just wrote:
# print(user_prompt.format(article="TEST-----").content)

## Let's create a propert prompt
title_generator_prompt_template=ChatPromptTemplate.from_messages(
    [
        system_prompt,
        title_generator_user_prompt
    ]
    )

#Test
# print(prompt_one.format(article="Test---"))

## Now that we have everything in place let's create a chain
title_generator_chain=  (
    ## Adding input varirables
    {"article":lambda x:x["article"]} 
    ### Adding prompt into the chain
    | title_generator_prompt_template 
    ## Adding LLM o in the chain
    | llm 
    ## Adding response_one format
    | {"article_title":lambda x: x.content}
)

##Now that we have created our chain let's invoke it 
response_one=title_generator_chain.invoke({
    "article":content
})

print(f"Title for this aritcle is {response_one['article_title']}")

####
# Getting Description for the article 
####


summary_generator_user_prompt = HumanMessagePromptTemplate.from_template(
    """You are tasked with creating a summary for
the article. The article is here for you to examine:

---

{article}

---

Here is the article title '{article_title}'.

Output the SEO friendly article summary. Do not output
anything other than the summary.""",
    input_variables=["article", "article_title"]
)

summary_prompt_template = ChatPromptTemplate.from_messages([
    system_prompt,
    summary_generator_user_prompt
])

summary_chain = (
    ## Chainging input variables i.e. adding one then perivous chain 
    {
        "article": lambda x: x["article"],
        "article_title": lambda x: x["article_title"]
    }

    ## CHainging the prompt 
    | summary_prompt_template

    ## keeping the llm as it is
    | llm

    ## chaining the output 
    | {"summary": lambda x: x.content}
)

## Invoking description chain
response_two=summary_chain.invoke({
    "article":content,
    "article_title":response_one['article_title']
})

print(response_two['summary'])


### User promtp 3
feedback_template_user_prompt = HumanMessagePromptTemplate.from_template(
    """You are tasked with creating a new paragraph for the
article. The article is here for you to examine:

---

{article}

---

Choose one paragraph to review and edit. During your edit
ensure you provide constructive feedback to the user so they
can learn where to improve their own writing.""",
    input_variables=["article"]
)

# prompt template 3: creating a new paragraph for the article
feedback_prompt_template = ChatPromptTemplate.from_messages([
    system_prompt,
    feedback_template_user_prompt
])

## Creating a pydantic model for output
class Paragraph(BaseModel):
    original_paragraph: str = Field(description="The original paragraph")
    edited_paragraph: str = Field(description="The improved edited paragraph")
    feedback: str = Field(description=(
        "Constructive feedback on the original paragraph"
    ))

structured_llm = llm.with_structured_output(Paragraph)

# review_chain=(
#             {
#                 "article":lambda x:x['article'],
#             }

#             |feedback_prompt_template

#             |llm 

#             |{"article_feedback":lambda c:c.content} 
#             )


# chain 3: inputs: article / output: article_para
feedback_chain = (
    {"article": lambda x: x["article"]}
    | feedback_prompt_template
    | structured_llm
    | {
        "original_paragraph": lambda x: x.original_paragraph,
        "edited_paragraph": lambda x: x.edited_paragraph,
        "feedback": lambda x: x.feedback
    }
)

response_three = feedback_chain.invoke({"article": content})
print(response_three)
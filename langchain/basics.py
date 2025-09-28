from langchain_openai import ChatOpenAI

from langchain_core.prompts import (
            SystemMessagePromptTemplate, 
            HumanMessagePromptTemplate,
            AIMessagePromptTemplate,
            ChatPromptTemplate
)

from dotenv import load_dotenv

load_dotenv()

with open("langchain/data/article.txt", "r") as f:
    content = f.read()



llm=ChatOpenAI(model="gpt-4o",temperature=0.9)

# Defining the system prompt (how the AI should behave)
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are an AI assistant that helps generate article titles."
)

# The user prompt is provided by the user, in this case however the only dynamic
# input is the article
user_prompt = HumanMessagePromptTemplate.from_template(
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
prompt_one=ChatPromptTemplate.from_messages([system_prompt,user_prompt])

#Test
# print(prompt_one.format(article="Test---"))

## Now that we have everything in place let's create a chain
chain_one=  (
    ## Adding input varirables
    {"article":lambda x:x["article"]} 
    ### Adding prompt into the chain
    | prompt_one 
    ## Adding LLM o in the chain
    | llm 
    ## Adding response format
    | {"article_title":lambda x: x.content}
)

##Now that we have created our chain let's invoke it 
response=chain_one.invoke({
    "article":content
})

print(f"Title for this aritcle is {response['article_title']}")
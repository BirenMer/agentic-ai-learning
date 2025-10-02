## Download file from the below command
# wget --user-agent "Mozilla" "https://arxiv.org/pdf/2312.04511.pdf" -O "llm_compiler.pdf"
# wget --user-agent "Mozilla" "https://arxiv.org/pdf/2312.06648.pdf" -O "dense_x_retrieval.pdf"

## In this file we reproduce the code form an official blog in llamaindex for testing Multi tanent RAG. 
 
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters, FilterOperator
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

from dotenv import load_dotenv
load_dotenv()


# Configure LLM
Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0)

# Configure embeddings
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

## Loading the data.
reader = SimpleDirectoryReader(input_files=['/home/biren/workspace/personal/agentic-ai-learning/multiteanent-rag/data/dense_x_retrieval.pdf'])
documents_jerry = reader.load_data()

reader = SimpleDirectoryReader(input_files=['/home/biren/workspace/personal/agentic-ai-learning/multiteanent-rag/data/llm_compiler.pdf'])
documents_ravi = reader.load_data()

## Creating a vector store index.
index = VectorStoreIndex.from_documents(documents=[])

## Creating an ingestion pip for querying the docs
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=512, chunk_overlap=20),
    ]
)

### There are two users and we are setting the data according to those users

# For user Jerry
for document in documents_jerry:
    document.metadata['user'] = 'Jerry'

nodes = pipeline.run(documents=documents_jerry)
# Insert nodes into the index
index.insert_nodes(nodes)

# For user Ravi
for document in documents_ravi:
    document.metadata['user'] = 'Ravi'

nodes = pipeline.run(documents=documents_ravi)
# Insert nodes into the index
index.insert_nodes(nodes)


## Creating separate query engines to ensure complete isolation of the chat in real time there would be n such engines.
jerry_query_engine = index.as_query_engine(
    # llm=OpenAI(model="gpt-4o-mini"),
    filters=MetadataFilters(filters=[ExactMatchFilter(key="user", value="Jerry")]),
    similarity_top_k=3
)

ravi_query_engine = index.as_query_engine(
    # llm=OpenAI(model="gpt-4o-mini"),
    filters=MetadataFilters(filters=[ExactMatchFilter(key="user", value="Ravi")]),
    similarity_top_k=3
)



# Jerry has Dense X Rerieval paper and should be able to answer following question.
jerry_response = jerry_query_engine.query(
    "what are propositions mentioned in the paper?"
)

# Ravi has LLMCompiler paper
ravi_response = ravi_query_engine.query("what are steps involved in LLMCompiler?")


print(jerry_response)
print(ravi_response)
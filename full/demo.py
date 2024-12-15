# Import the necessary modules
from dotenv import load_dotenv
import os
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings

load_dotenv("/app/.env")

db_name = "langchain_demo"
collection_name = "chunked_data"
index = "vector_index"
connection_string = os.getenv("CONNECTION_STRING")

# Create the vector store
vector_store = MongoDBAtlasVectorSearch.from_connection_string(
    connection_string=connection_string,
    namespace=f"{db_name}.{collection_name}",
    embedding=OpenAIEmbeddings(disallowed_special=(),
        openai_api_key="mock_openai_key"),
    index_name=index,
)


# Define the query_data function
def query_data(query):
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3},
    )
    results = retriever.invoke(query)
    print(results)


# Query the data
query_data("When did MongoDB begin supporting multi-document transactions?")
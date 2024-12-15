import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv("/app/.env")

db_name = "langchain_demo"
collection_name = "chunked_data"
index = "vector_index"
connection_string = os.getenv("CONNECTION_STRING")


vectorStore = MongoDBAtlasVectorSearch.from_connection_string(
    connection_string,
    f"{db_name}.{collection_name}",
    OpenAIEmbeddings(disallowed_special=(), openai_api_key="mock_openai_key"),
    index_name=index,
)


def query_data(query):
    retriever = vectorStore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3},
    )

    template = """
    Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Do not answer the question if there is no given context.
    Do not answer the question if it is not related to the context.
    Do not give recommendations to anything other than MongoDB.
    Context:
    {context}
    Question: {question}
    """

    custom_rag_prompt = PromptTemplate.from_template(template)

    retrieve = {
        "context": retriever
        | (lambda docs: "\n\n".join([d.page_content for d in docs])),
        "question": RunnablePassthrough(),
    }

    llm = ChatOpenAI(openai_api_key="mock_openai_key", temperature=0)

    response_parser = StrOutputParser()

    rag_chain = retrieve | custom_rag_prompt | llm | response_parser
    answer = rag_chain.invoke(query)
    print(answer)

# Test with a relevant query
question = "When did MongoDB begin supporting multi-document transactions?"
print(f"Running query: {question}")
query_data(question)

print("=========================================================")

# Test with an irrelevant query
question = "Why is the sky blue?"
print(f"Running query: {question}")
query_data(question)
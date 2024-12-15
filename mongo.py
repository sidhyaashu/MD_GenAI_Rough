"""
Prerequisites

Atlas Cluster Connecting String
OpenAI API Key


pip3 install langchain langchain_community langchain_core langchain_openai langchain_mongodb pymongo pypdf


MONGODB_URI=<your_atlas_connection_string>
LLM_API_KEY=<your_llm_api_key>
"""

from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_transformers.openai_functions import (
    create_metadata_tagger,
)

import key_param

# Set the MongoDB URI, DB, Collection Names

client = MongoClient(key_param.MONGODB_URI)
dbName = "book_mongodb_chunks"
collectionName = "chunked_data"
collection = client[dbName][collectionName]

loader = PyPDFLoader(".\sample_files\mongodb.pdf")
pages = loader.load()
cleaned_pages = []

for page in pages:
    if len(page.page_content.split(" ")) > 20:
        cleaned_pages.append(page)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=150)

schema = {
    "properties": {
        "title": {"type": "string"},
        "keywords": {"type": "array", "items": {"type": "string"}},
        "hasCode": {"type": "boolean"},
    },
    "required": ["title", "keywords", "hasCode"],
}

llm = ChatOpenAI(
    openai_api_key=key_param.LLM_API_KEY, temperature=0, model="gpt-3.5-turbo"
)

document_transformer = create_metadata_tagger(metadata_schema=schema, llm=llm)

docs = document_transformer.transform_documents(cleaned_pages)

split_docs = text_splitter.split_documents(docs)

embeddings = OpenAIEmbeddings(openai_api_key=key_param.LLM_API_KEY)


vectorStore = MongoDBAtlasVectorSearch.from_documents(
    split_docs, embeddings, collection=collection
)
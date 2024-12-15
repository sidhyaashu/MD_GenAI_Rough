import os

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from create_metadata_tagger import create_metadata_tagger
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pymongo import MongoClient

# Load the environment variables
load_dotenv('/app/.env')

# Initialize the MongoDB client for storing the chunked data
client = MongoClient(os.getenv("CONNECTION_STRING"))
collection = client["langchain_demo"]["chunked_data"]

# Drop the database before adding new data
print("Deleting the collection before adding new data")
collection.delete_many({})

loader = PyPDFLoader("/lab/mongodb.pdf")
pages = loader.load()
cleaned_pages = []

for page in pages:
    if len(page.page_content.split(" ")) > 20:
        cleaned_pages.append(page)

print("Splitting the documents into chunks")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
  chunk_overlap=150)

schema = {
    "properties": {
        "title": {"type": "string"},
        "keywords": {"type": "array", "items": {"type": "string"}},
        "hasCode": {"type": "boolean"},
    },
    "required": ["title", "keywords", "hasCode"],
}

print("Creating metadata for the documents")
mock_openai_key = "mock_openai_key"
llm = ChatOpenAI(openai_api_key=mock_openai_key, temperature=0,
  model="gpt-4o-mini")
document_transformer = create_metadata_tagger(schema, llm)
docs = document_transformer.transform_documents(cleaned_pages)
split_docs = text_splitter.split_documents(docs)

# Generate the vector embeddings
print("Generating vector embeddings for the documents")
embeddings = OpenAIEmbeddings(openai_api_key=mock_openai_key)

# Store the vectors in MongoDB Atlas
print("Storing the vectors in MongoDB Atlas")
vector_store = MongoDBAtlasVectorSearch.from_documents(
    split_docs, embeddings, collection=collection
)

document_count = collection.count_documents({})
print(f"Successfully stored {document_count} documents in MongoDB Atlas")
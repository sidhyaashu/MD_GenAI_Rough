from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from create_metadata_tagger import create_metadata_tagger
from langchain_openai import ChatOpenAI
from pymongo import MongoClient

loader = PyPDFLoader("/lab/mongodb.pdf")
pages = loader.load()
cleaned_pages = []

for page in pages:
    if len(page.page_content.split(" ")) > 20:
        cleaned_pages.append(page)

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

mock_openai_key = "mock_openai_key"
llm = ChatOpenAI(openai_api_key=mock_openai_key, temperature=0,
    model="gpt-4o-mini")
document_transformer = create_metadata_tagger(schema, llm)
docs = document_transformer.transform_documents(cleaned_pages)

split_docs = text_splitter.split_documents(docs)

print(split_docs[0])
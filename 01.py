from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pymongo import MongoClient

loader = PyPDFLoader('/lab/mongodb.pdf')
pages = loader.load()
cleaned_pages = []

for page in pages:
    if len(page.page_content.split(" ")) > 20:
        cleaned_pages.append(page)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
  chunk_overlap=150)
split_docs = text_splitter.split_documents(cleaned_pages)

print(split_docs[21])
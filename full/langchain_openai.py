import json
from typing import List

from langchain_core.embeddings import Embeddings
from langchain_core.pydantic_v1 import BaseModel
embeddings_file = "/lab/embeddings.json"
query_embeddings_file ="/lab/query_embeddings.json"

class OpenAIEmbeddings():
    """Fake embedding model."""

    def __init__(self, openai_api_key, disallowed_special=()):
        self.openai_api_key = openai_api_key

    def _get_embedding(self) -> List[float]:
        with open(query_embeddings_file, "r") as file:
            embeddings = json.load(file)     
        return embeddings['query_embeddings']
  
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        with open(embeddings_file, "r") as file:
            embeddings = json.load(file)     
        return embeddings['embeddings']

    def embed_query(self, text:str) -> List[float]:
        return self._get_embedding()

class ChatOpenAI:
    def __init__(self, openai_api_key, temperature=0, model="gpt-4o-mini"):
        self.openai_api_key = openai_api_key
        self.temperature = temperature
        self.model = model
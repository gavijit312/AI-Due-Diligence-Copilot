from typing import List, Optional
import chromadb
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from config.settings import settings


class VectorStoreService:
    def __init__(self, collection_name: str = "duesense_docs"):
        self.collection_name = collection_name
        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            api_key=settings.OPENAI_API_KEY
        )
        self.client = chromadb.PersistentClient(path=str(settings.CHROMA_PERSIST_DIR))
        self.store = Chroma(
            client=self.client,
            collection_name=self.collection_name,
            embedding_function=self.embeddings
        )

    def add_documents(self, documents: List[Document]) -> List[str]:
        if not documents:
            return []
        return self.store.add_documents(documents)

    def similarity_search_by_category(
        self,
        query: str,
        category: Optional[str] = None,
        k: int = 5
    ) -> List[Document]:
        filter_dict = {"category": category} if category else None
        return self.store.similarity_search(query, k=k, filter=filter_dict)


vector_service = VectorStoreService()
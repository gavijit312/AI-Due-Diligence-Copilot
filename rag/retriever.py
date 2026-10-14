from typing import List, Optional
from langchain_core.documents import Document
from core.vector_store import vector_service


class DueDiligenceRetriever:
    def __init__(self, top_k: int = 6):
        self.top_k = top_k
        self.vector_store = vector_service

    def retrieve(
        self,
        query: str,
        category: Optional[str] = None,
        top_k: Optional[int] = None
    ) -> List[Document]:
        k = top_k or self.top_k
        return self.vector_store.similarity_search_by_category(
            query=query,
            category=category,
            k=k
        )


retriever = DueDiligenceRetriever()
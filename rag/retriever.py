"""
Document retrieval module for DueSense AI.

Loads the persisted FAISS index and retrieves relevant document
chunks for a user's question.
"""

from pathlib import Path
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from config.settings import TOP_K, VECTOR_DB_PATH
from rag.vector_store import load_vector_store


def get_retriever(
    vector_store: FAISS,
    top_k: int = TOP_K,
):
    """Create a retriever from an existing FAISS vector store."""

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k},
    )


def retrieve_documents(
    query: str,
    vector_store: FAISS | None = None,
    top_k: int = TOP_K,
) -> List[Document]:
    """
    Retrieve relevant document chunks for a question.

    If no vector store is supplied, load the persisted FAISS index.
    """

    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    if vector_store is None:
        vector_store = load_vector_store(Path(VECTOR_DB_PATH))

    retriever = get_retriever(vector_store, top_k=top_k)

    return retriever.invoke(query.strip())


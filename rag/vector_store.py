"""
FAISS vector store for DueSense AI.

Creates, saves, loads, and searches vector indexes.
"""

from pathlib import Path
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from rag.embeddings import get_embeddings


def create_vector_store(
    documents: List[Document],
) -> FAISS:
    """Create a FAISS index from document chunks."""

    if not documents:
        raise ValueError(
            "Cannot create a vector store without documents."
        )

    embeddings = get_embeddings()

    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embeddings,
    )

    return vector_store


def save_vector_store(
    vector_store: FAISS,
    db_path: str | Path,
) -> None:
    """Save the FAISS index to disk."""

    path = Path(db_path)
    path.mkdir(parents=True, exist_ok=True)

    vector_store.save_local(str(path))

    print(f"FAISS vector store saved to: {path.resolve()}")


def load_vector_store(
    db_path: str | Path,
) -> FAISS:
    """Load a previously saved FAISS index."""

    path = Path(db_path)

    index_file = path / "index.faiss"
    metadata_file = path / "index.pkl"

    if not index_file.is_file() or not metadata_file.is_file():
        raise FileNotFoundError(
            f"No complete FAISS index found at {path.resolve()}. "
            "Create and save the vector store first."
        )

    embeddings = get_embeddings()

    # Only load indexes created by a trusted source.
    return FAISS.load_local(
        str(path),
        embeddings,
        allow_dangerous_deserialization=True,
    )


def search_vector_store(
    vector_store: FAISS,
    query: str,
    top_k: int = 5,
) -> List[Document]:
    """Return the most relevant chunks for a query."""

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    results = vector_store.similarity_search(
        query=query,
        k=top_k,
    )

    return results


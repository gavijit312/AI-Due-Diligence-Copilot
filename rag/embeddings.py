"""
Embedding module for DueSense AI.

Converts document text into numerical vectors for semantic search.
Uses a local Sentence Transformers model on the CPU.
"""

from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

from config.settings import EMBEDDING_MODEL


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    """
    Load and cache the embedding model.

    The model is initialized only once per Python process.
    """

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def embed_text(text: str) -> list[float]:
    """
    Convert a single text string into an embedding vector.
    """

    if not text or not text.strip():
        raise ValueError("Cannot embed empty text.")

    return get_embeddings().embed_query(text)


def embed_documents(texts: list[str]) -> list[list[float]]:
    """
    Convert multiple text strings into embedding vectors.
    """

    if not texts:
        raise ValueError("No texts provided for embedding.")

    if any(not text or not text.strip() for text in texts):
        raise ValueError("Input texts must not contain empty strings.")

    return get_embeddings().embed_documents(texts)


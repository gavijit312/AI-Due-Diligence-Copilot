

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import CHUNK_SIZE, CHUNK_OVERLAP


def get_text_splitter() -> RecursiveCharacterTextSplitter:
    """
    Create and return the configured text splitter.
    """

    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
        add_start_index=True,
    )


def split_documents(
    documents: List[Document],
) -> List[Document]:
    """
    Split documents into smaller chunks.

    Each chunk retains the original metadata and receives:
        - chunk_id: Unique ID within this splitting operation
        - start_index: Character position in the original page
    """

    if not documents:
        raise ValueError(
            "No documents provided for chunking."
        )

    splitter = get_text_splitter()
    chunks = splitter.split_documents(documents)

    for index, chunk in enumerate(chunks, start=1):
        chunk.metadata["chunk_id"] = index

    if not chunks:
        raise ValueError(
            "The text splitter did not produce any chunks."
        )

    return chunks

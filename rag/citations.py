from typing import List, Dict, Any
from langchain_core.documents import Document


def format_citations(documents: List[Document]) -> List[Dict[str, Any]]:
    citations = []
    for doc in documents:
        citations.append({
            "source": doc.metadata.get("source", "Unknown"),
            "page": doc.metadata.get("page", 1),
            "category": doc.metadata.get("category", "General"),
            "excerpt": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
        })
    return citations


def build_cited_context(documents: List[Document]) -> str:
    blocks = []
    for idx, doc in enumerate(documents, start=1):
        source = doc.metadata.get("source", "doc")
        page = doc.metadata.get("page", 1)
        category = doc.metadata.get("category", "general")
        blocks.append(
            f"[{idx}] Source: {source} | Page: {page} | Domain: {category}\nContent: {doc.page_content}"
        )
    return "\n\n".join(blocks)
from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_extracted_pages(
    pages: List[Dict[str, Any]],
    source_filename: str,
    category: str
) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=250,
        separators=["\n\n", "\n", " ", ""]
    )
    documents = []

    for page_item in pages:
        page_num = page_item["page"]
        raw_text = page_item["text"]

        if not raw_text.strip():
            continue

        chunks = splitter.split_text(raw_text)
        for idx, chunk in enumerate(chunks):
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "source": source_filename,
                        "category": category,
                        "page": page_num,
                        "chunk_index": idx
                    }
                )
            )

    return documents
"""
PDF document loader for the DueSense AI RAG pipeline.

Extracts text page by page and preserves source metadata.
"""

from pathlib import Path
from typing import List

import pymupdf
from langchain_core.documents import Document


def load_pdf(file_path: str | Path) -> List[Document]:
    """
    Load a PDF and return one Document per page containing extractable text.

    Each Document stores:
        - source: PDF filename
        - file_path: Absolute path to the PDF
        - page: One-based page number
    """

    pdf_path = Path(file_path)

    if not pdf_path.is_file():
        raise FileNotFoundError(
            f"PDF file not found: {pdf_path}"
        )

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(
            f"Unsupported file type: {pdf_path.suffix}. "
            "Only PDF files are supported."
        )

    documents: List[Document] = []

    with pymupdf.open(str(pdf_path)) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text("text").strip()

            # Skip pages without extractable text.
            if not text:
                continue

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": pdf_path.name,
                        "file_path": str(pdf_path.resolve()),
                        "page": page_number,
                    },
                )
            )

    if not documents:
        raise ValueError(
            f"No extractable text found in {pdf_path.name}. "
            "The PDF may be scanned and require OCR."
        )

    return documents


def load_documents(directory: str | Path) -> List[Document]:
    """
    Load all PDFs from a directory.

    Returns a list of page-level Documents.
    """

    directory_path = Path(directory)

    if not directory_path.is_dir():
        raise FileNotFoundError(
            f"Directory not found: {directory_path}"
        )

    pdf_files = sorted(directory_path.glob("*.pdf"))

    if not pdf_files:
        raise ValueError(
            f"No PDF files found in {directory_path}"
        )

    all_documents: List[Document] = []

    for pdf_file in pdf_files:
        try:
            documents = load_pdf(pdf_file)
            all_documents.extend(documents)

            print(
                f"Loaded {pdf_file.name}: "
                f"{len(documents)} pages"
            )

        except Exception as error:
            print(
                f"Failed to load {pdf_file.name}: {error}"
            )

    if not all_documents:
        raise ValueError(
            "No PDF documents could be loaded successfully."
        )

    return all_documents
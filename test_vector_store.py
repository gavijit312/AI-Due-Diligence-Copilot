from config.settings import UPLOAD_FOLDER, VECTOR_DB_PATH
from rag.loader import load_documents
from rag.chunker import split_documents
from rag.vector_store import (
    create_vector_store,
    save_vector_store,
    load_vector_store,
    search_vector_store,
)


def main():
    print("STEP 1: Loading PDF documents...")

    documents = load_documents(UPLOAD_FOLDER)
    print(f"Pages loaded: {len(documents)}")

    print("\nSTEP 2: Splitting documents into chunks...")

    chunks = split_documents(documents)
    print(f"Chunks created: {len(chunks)}")

    print("\nSTEP 3: Creating FAISS vector store...")

    vector_store = create_vector_store(chunks)
    print("FAISS index created successfully.")

    print("\nSTEP 4: Saving the vector store...")

    save_vector_store(vector_store, VECTOR_DB_PATH)

    print("\nSTEP 5: Loading the saved vector store...")

    loaded_store = load_vector_store(VECTOR_DB_PATH)
    print("FAISS index loaded successfully.")

    print("\nSTEP 6: Searching for relevant passages...")

    query = "Who owns the intellectual property before payment?"
    results = search_vector_store(
        vector_store=loaded_store,
        query=query,
        top_k=3,
    )

    print(f"\nQuery: {query}")

    for index, document in enumerate(results, start=1):
        print("\n" + "=" * 70)
        print(f"Result {index}")
        print(f"Source: {document.metadata.get('source')}")
        print(f"Page: {document.metadata.get('page')}")
        print("\nRetrieved text:")
        print(document.page_content[:500])

    print("\nVECTOR STORE TEST SUCCESSFUL")


if __name__ == "__main__":
    main()

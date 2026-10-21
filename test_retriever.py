from rag.retriever import retrieve_documents


def main():
    query = "Who owns the intellectual property before payment?"

    print("Testing DueSense AI document retrieval...")
    print(f"\nQuestion: {query}")

    documents = retrieve_documents(query, top_k=3)

    if not documents:
        print("\nNo relevant documents were retrieved.")
        return

    for index, document in enumerate(documents, start=1):
        print("\n" + "=" * 70)
        print(f"Result {index}")
        print(f"Source: {document.metadata.get('source', 'Unknown')}")
        print(f"Page: {document.metadata.get('page', 'Unknown')}")
        print(f"Chunk ID: {document.metadata.get('chunk_id', 'Unknown')}")
        print("\nRetrieved text:")
        print(document.page_content[:500])

    print("\nRETRIEVER TEST SUCCESSFUL")


if __name__ == "__main__":
    main()

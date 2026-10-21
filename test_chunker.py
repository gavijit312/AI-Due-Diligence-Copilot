from rag.loader import load_documents
from rag.chunker import split_documents

UPLOAD_FOLDER = "data/uploads"

try:
    # Step 1: Load PDF pages.
    documents = load_documents(UPLOAD_FOLDER)

    print(f"\nOriginal pages loaded: {len(documents)}")

    # Step 2: Split the pages into chunks.
    chunks = split_documents(documents)

    print(f"Total chunks created: {len(chunks)}")

    # Step 3: Display chunk details.
    for chunk in chunks:
        print("\n" + "=" * 70)
        print(f"Chunk ID: {chunk.metadata['chunk_id']}")
        print(f"Source: {chunk.metadata.get('source')}")
        print(f"Page: {chunk.metadata.get('page')}")
        print(f"Start index: {chunk.metadata.get('start_index')}")
        print(f"Characters: {len(chunk.page_content)}")

        print("\nText preview:")
        print(chunk.page_content[:300])

    print("\nCHUNKER TEST SUCCESSFUL")

except Exception as error:
    print(f"\nCHUNKER TEST FAILED: {error}")


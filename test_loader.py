from rag.loader import load_documents

UPLOAD_FOLDER = "data/uploads"

try:
    documents = load_documents(UPLOAD_FOLDER)

    print("\nPDF LOADER TEST SUCCESSFUL")
    print(f"Total pages loaded: {len(documents)}")

    first_document = documents[0]

    print("\nFirst page metadata:")
    print(first_document.metadata)

    print("\nFirst page text preview:")
    print(first_document.page_content[:500])

except Exception as error:
    print(f"\nPDF LOADER TEST FAILED: {error}")
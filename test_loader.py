
from rag.loader import load_documents

UPLOAD_FOLDER = "data/uploads"

try:
    documents = load_documents(UPLOAD_FOLDER)

    print("\nPDF LOADER TEST SUCCESSFUL")
    print(f"Total pages loaded: {len(documents)}")

    for index, document in enumerate(documents, start=1):
        print("\n" + "=" * 80)
        print(f"PAGE {index}")
        print("=" * 80)

        print(f"Source: {document.metadata['source']}")
        print(f"Page number: {document.metadata['page']}")
        print(f"Extracted characters: {len(document.page_content)}")

        print("\nCOMPLETE EXTRACTED TEXT:\n")
        print(document.page_content)

    print("\n" + "=" * 80)
    print("ALL PAGES DISPLAYED SUCCESSFULLY")
    print("=" * 80)

except Exception as error:
    print(f"\nPDF LOADER TEST FAILED: {error}")


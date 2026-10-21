from rag.embeddings import embed_text, embed_documents

try:
    # Test a single text.
    text = (
        "The provider retains intellectual property ownership "
        "until the required contractual payments are completed."
    )

    vector = embed_text(text)

    print("SINGLE TEXT EMBEDDING TEST")
    print(f"Vector dimensions: {len(vector)}")
    print(f"First five values: {vector[:5]}")

    # Test multiple texts.
    texts = [
        "The provider retains intellectual property rights.",
        "The agreement requires payment within thirty days.",
        "The company must maintain confidentiality.",
    ]

    vectors = embed_documents(texts)

    print("\nMULTIPLE TEXT EMBEDDING TEST")
    print(f"Texts processed: {len(vectors)}")
    print(f"Vector dimensions: {len(vectors[0])}")

    assert len(vector) == 384
    assert len(vectors) == len(texts)
    assert all(len(item) == 384 for item in vectors)

    print("\nEMBEDDING TEST SUCCESSFUL")

except Exception as error:
    print(f"\nEMBEDDING TEST FAILED: {error}")
    raise

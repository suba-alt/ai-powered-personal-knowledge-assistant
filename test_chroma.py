from services.chroma_service import collection


print("================================")
print("CHROMADB STORAGE TEST")
print("================================")

print("Collection name:", collection.name)

count = collection.count()

print("Total stored chunks:", count)


if count == 0:
    print("\n❌ ChromaDB is empty.")
    print("Upload a document first.")
else:
    print("\n✅ ChromaDB contains data.")

    results = collection.get(
        include=[
            "documents",
            "metadatas",
            "embeddings"
        ]
    )

    ids = results.get("ids", [])
    documents = results.get("documents", [])
    metadatas = results.get("metadatas", [])
    embeddings = results.get("embeddings", [])

    for i in range(len(ids)):

        print("\n-----------------------------")
        print("CHUNK", i + 1)
        print("-----------------------------")

        print("ID:", ids[i])

        print("File:",
              metadatas[i].get("file_name"))

        print("Document ID:",
              metadatas[i].get("document_id"))

        print("User ID:",
              metadatas[i].get("user_id"))

        print("Chunk ID:",
              metadatas[i].get("chunk_id"))

        print("\nText:")
        print(documents[i][:300])

    if len(embeddings) > 0:

        print("\nEmbedding dimension:",
          len(embeddings[i]))

        print("First 5 values:",
          embeddings[i][:5])
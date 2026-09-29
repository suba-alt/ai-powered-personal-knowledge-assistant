from services.chroma_service import search_documents


question = "What is software testing?"


print("================================")
print("CHROMADB RETRIEVAL TEST")
print("================================")

print("\nQuestion:")
print(question)


results = search_documents(
    question=question,
    user_id=1,
    top_k=5
)


print("\nNumber of results:")
print(len(results))


for index, result in enumerate(results, start=1):

    print("\n================================")
    print(f"RESULT {index}")
    print("================================")

    print("Document ID:")
    print(result.get("document_id"))

    print("\nFile name:")
    print(result.get("file_name"))

    print("\nChunk ID:")
    print(result.get("chunk_id"))

    print("\nDistance:")
    print(result.get("distance"))

    print("\nText:")
    print(result.get("text"))
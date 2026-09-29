from services.chroma_service import collection
from services.embedding_service import generate_embedding


question = "What is software testing?"

print("================================")
print("CHROMADB DEBUG TEST")
print("================================")

print("Collection:", collection.name)
print("Total chunks:", collection.count())


# Generate query embedding
query_embedding = generate_embedding(question)

print("\nQuery embedding generated")
print("Embedding dimension:", len(query_embedding))


# ------------------------------------------
# TEST 1: SEARCH WITHOUT USER FILTER
# ------------------------------------------

print("\n================================")
print("TEST 1 - WITHOUT USER FILTER")
print("================================")

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5,
    include=[
        "documents",
        "metadatas",
        "distances"
    ]
)

documents = results.get("documents", [[]])[0]
metadatas = results.get("metadatas", [[]])[0]
distances = results.get("distances", [[]])[0]

print("Results:", len(documents))


for i in range(len(documents)):

    print("\n-----------------------------")
    print("RESULT", i + 1)
    print("-----------------------------")

    print("Distance:", distances[i])

    print("Metadata:")
    print(metadatas[i])

    print("\nText:")
    print(documents[i][:300])


# ------------------------------------------
# TEST 2: SEARCH WITH USER ID
# ------------------------------------------

print("\n================================")
print("TEST 2 - WITH USER ID 15")
print("================================")

results_user = collection.query(
    query_embeddings=[query_embedding],
    n_results=5,

    where={
        "user_id": "15"
    },

    include=[
        "documents",
        "metadatas",
        "distances"
    ]
)

documents_user = results_user.get(
    "documents",
    [[]]
)[0]

metadatas_user = results_user.get(
    "metadatas",
    [[]]
)[0]

distances_user = results_user.get(
    "distances",
    [[]]
)[0]

print("Results:", len(documents_user))


for i in range(len(documents_user)):

    print("\n-----------------------------")
    print("RESULT", i + 1)
    print("-----------------------------")

    print("Distance:", distances_user[i])

    print("Metadata:")
    print(metadatas_user[i])

    print("\nText:")
    print(documents_user[i][:300])
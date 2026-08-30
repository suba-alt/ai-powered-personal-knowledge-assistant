import os
import chromadb

from services.embedding_service import (
    generate_embedding
)


# ==========================================
# CHROMADB CONFIGURATION
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


CHROMA_PATH = os.path.join(
    BASE_DIR,
    "chroma_db"
)


COLLECTION_NAME = "documents"


# ==========================================
# CHROMADB CLIENT
# ==========================================

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


# ==========================================
# COLLECTION
# ==========================================

collection = client.get_or_create_collection(

    name=COLLECTION_NAME,

    metadata={
        "description":
            "AI Knowledge Assistant documents"
    }
)


# ==========================================
# CHUNK TEXT
# ==========================================

def create_chunks(
    text,
    chunk_size=500,
    overlap=50
):

    if not text:

        return []

    text = text.strip()

    chunks = []

    start = 0

    text_length = len(text)

    while start < text_length:

        end = start + chunk_size

        chunk = text[
            start:end
        ].strip()

        if chunk:

            chunks.append(
                chunk
            )

        next_start = (
            end - overlap
        )

        if next_start <= start:

            break

        start = next_start

    return chunks


# ==========================================
# ADD DOCUMENT TO CHROMADB
# ==========================================

def add_document(
    document_id,
    user_id,
    file_name,
    text
):

    chunks = create_chunks(
        text
    )

    if not chunks:

        raise ValueError(
            "No text chunks found"
        )

    ids = []

    embeddings = []

    documents = []

    metadatas = []

    for index, chunk in enumerate(chunks):

        chunk_id = (
            f"document_{document_id}_"
            f"chunk_{index}"
        )

        embedding = generate_embedding(
            chunk
        )

        ids.append(
            chunk_id
        )

        embeddings.append(
            embedding
        )

        documents.append(
            chunk
        )

        metadatas.append({

            "document_id":
                str(document_id),

            "user_id":
                str(user_id),

            "file_name":
                file_name,

            "chunk_id":
                str(index)

        })

    collection.upsert(

        ids=ids,

        embeddings=embeddings,

        documents=documents,

        metadatas=metadatas

    )

    return {

        "document_id":
            document_id,

        "chunks_stored":
            len(chunks)

    }


# ==========================================
# SEARCH CHROMADB
# ==========================================

def search_documents(
    question,
    user_id,
    top_k=5
):

    query_embedding = generate_embedding(
        question
    )

    results = collection.query(

        query_embeddings=[
            query_embedding
        ],

        n_results=top_k,

        where={

            "user_id":
                str(user_id)

        },

        include=[
            "documents",
            "metadatas",
            "distances"
        ]

    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    search_results = []

    for index, text in enumerate(
        documents
    ):

        metadata = metadatas[index]

        distance = distances[index]

        search_results.append({

            "text":
                text,

            "document_id":
                metadata.get(
                    "document_id"
                ),

            "user_id":
                metadata.get(
                    "user_id"
                ),

            "file_name":
                metadata.get(
                    "file_name"
                ),

            "chunk_id":
                metadata.get(
                    "chunk_id"
                ),

            "distance":
                distance

        })

    return search_results


# ==========================================
# DELETE DOCUMENT FROM CHROMADB
# ==========================================

def delete_document(
    document_id
):

    collection.delete(

        where={

            "document_id":
                str(document_id)

        }

    )
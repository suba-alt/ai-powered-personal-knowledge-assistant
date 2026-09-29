import os
import chromadb

from services.embedding_service import (
    generate_embeddings,
    generate_query_embedding
)


# ============================================================
# CHROMADB CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

CHROMA_PATH = os.path.join(
    BASE_DIR,
    "chroma_db"
)

COLLECTION_NAME = "documents_minilm_384"


# ============================================================
# CHROMADB CLIENT
# ============================================================

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


# ============================================================
# COLLECTION
# ============================================================

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={
        "description":
            "AI Knowledge Assistant documents "
            "using MiniLM 384-dimensional embeddings",

        "hnsw:space":
            "cosine"
    }
)


# ============================================================
# CREATE TEXT CHUNKS
# ============================================================

def create_chunks(
    text,
    chunk_size=500,
    overlap=50
):

    if not text:
        return []

    text = text.strip()

    if not text:
        return []

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        next_start = end - overlap

        if next_start <= start:
            break

        start = next_start

    return chunks


# ============================================================
# DEBUG CHROMADB DATA
# ============================================================

def debug_chroma_data():

    print("\n")
    print("==================================================")
    print("CHROMADB DEBUG")
    print("==================================================")

    total = collection.count()

    print(
        f"TOTAL CHUNKS IN COLLECTION: {total}",
        flush=True
    )

    if total == 0:

        print(
            "ChromaDB collection is empty.",
            flush=True
        )

        print("==================================================")
        return

    try:

        results = collection.get(
            limit=min(10, total),
            include=[
                "documents",
                "metadatas"
            ]
        )

        metadatas = results.get(
            "metadatas",
            []
        )

        documents = results.get(
            "documents",
            []
        )

        print("\nSTORED METADATA:")

        for index, metadata in enumerate(metadatas):

            print(
                f"[{index}] {metadata}",
                flush=True
            )

        print("\nSTORED DOCUMENT PREVIEWS:")

        for index, document in enumerate(documents):

            preview = document[:200] if document else ""

            print(
                f"[{index}] {preview}",
                flush=True
            )

    except Exception as error:

        print(
            "CHROMADB DEBUG ERROR:",
            repr(error),
            flush=True
        )

    print("==================================================")
    print("\n")


# ============================================================
# ADD DOCUMENT
# ============================================================

def add_document(
    document_id,
    user_id,
    file_name,
    text
):

    print(
        "CHROMA STEP 1: Creating chunks",
        flush=True
    )

    chunks = create_chunks(
        text
    )

    print(
        f"CHROMA STEP 2: Chunks created: "
        f"{len(chunks)}",
        flush=True
    )

    if not chunks:

        raise ValueError(
            "No text chunks found"
        )

    # --------------------------------------------------------
    # CREATE IDS + DOCUMENTS + METADATA
    # --------------------------------------------------------

    ids = []
    documents = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        chunk_id = (
            f"document_{document_id}_chunk_{index}"
        )

        ids.append(
            chunk_id
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

    # --------------------------------------------------------
    # GENERATE MINILM EMBEDDINGS
    # --------------------------------------------------------

    print(
        "CHROMA STEP 3: Starting MiniLM embeddings",
        flush=True
    )

    embeddings = generate_embeddings(
        chunks
    )

    print(
        f"CHROMA STEP 4: MiniLM embeddings completed. "
        f"Embeddings: {len(embeddings)}",
        flush=True
    )

    # --------------------------------------------------------
    # VALIDATE EMBEDDINGS
    # --------------------------------------------------------

    if not embeddings:

        raise ValueError(
            "No embeddings generated"
        )

    if len(embeddings) != len(chunks):

        raise ValueError(
            "Number of embeddings does not "
            "match number of chunks"
        )

    for embedding in embeddings:

        if len(embedding) != 384:

            raise ValueError(
                f"Invalid embedding dimension: "
                f"{len(embedding)}. "
                f"Expected 384."
            )

    # --------------------------------------------------------
    # STORE IN CHROMADB
    # --------------------------------------------------------

    print(
        "CHROMA STEP 5: Starting ChromaDB upsert",
        flush=True
    )

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )

    print(
        "CHROMA STEP 6: ChromaDB upsert completed",
        flush=True
    )

    return {

        "document_id":
            document_id,

        "chunks_stored":
            len(chunks),

        "embedding_dimension":
            384
    }


# ============================================================
# SEARCH DOCUMENTS
# ============================================================

def search_documents(
    question,
    user_id,
    top_k=5
):

    # --------------------------------------------------------
    # VALIDATE QUESTION
    # --------------------------------------------------------

    if not question or not question.strip():

        raise ValueError(
            "Search query cannot be empty"
        )

    question = question.strip()

    # --------------------------------------------------------
    # VALIDATE USER
    # --------------------------------------------------------

    if user_id is None:

        raise ValueError(
            "User ID is required"
        )

    # --------------------------------------------------------
    # PRINT USER INFORMATION
    # --------------------------------------------------------

    print(
        f"SEARCH USER ID: {user_id}",
        flush=True
    )

    print(
        f"SEARCH USER ID TYPE: {type(user_id)}",
        flush=True
    )

    print(
        f"SEARCH USER ID AS STRING: {str(user_id)}",
        flush=True
    )

    # --------------------------------------------------------
    # VALIDATE TOP K
    # --------------------------------------------------------

    try:

        top_k = int(
            top_k
        )

    except (
        TypeError,
        ValueError
    ):

        top_k = 5

    top_k = max(
        1,
        min(
            top_k,
            10
        )
    )

    # --------------------------------------------------------
    # CHECK COLLECTION
    # --------------------------------------------------------

    collection_count = collection.count()

    print(
        f"SEARCH STEP 0: ChromaDB chunks = "
        f"{collection_count}",
        flush=True
    )

    if collection_count == 0:

        print(
            "SEARCH STEP 0: Collection is empty",
            flush=True
        )

        return []

    # --------------------------------------------------------
    # DEBUG STORED DATA
    # --------------------------------------------------------

    debug_chroma_data()

    # --------------------------------------------------------
    # GENERATE QUERY EMBEDDING
    # --------------------------------------------------------

    print(
        "SEARCH STEP 1: Generating MiniLM query embedding",
        flush=True
    )

    query_embedding = generate_query_embedding(
        question
    )

    print(
        "SEARCH STEP 2: Query embedding generated",
        flush=True
    )

    # --------------------------------------------------------
    # VALIDATE QUERY EMBEDDING
    # --------------------------------------------------------

    if not query_embedding:

        raise ValueError(
            "Query embedding was not generated"
        )

    if len(query_embedding) != 384:

        raise ValueError(
            f"Invalid query embedding dimension: "
            f"{len(query_embedding)}. "
            f"Expected 384."
        )

    # --------------------------------------------------------
    # CHROMADB SEARCH
    # --------------------------------------------------------

    print(
        "SEARCH STEP 3: Searching ChromaDB",
        flush=True
    )

    user_filter = {
        "user_id": str(user_id)
    }

    print(
        f"SEARCH FILTER: {user_filter}",
        flush=True
    )

    results = collection.query(

        query_embeddings=[
            query_embedding
        ],

        n_results=min(
            top_k,
            collection_count
        ),

        where=user_filter,

        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    print(
        "SEARCH STEP 4: ChromaDB search completed",
        flush=True
    )

    # --------------------------------------------------------
    # PRINT RAW RESULT INFORMATION
    # --------------------------------------------------------

    print(
        "RAW CHROMADB RESULTS:",
        flush=True
    )

    print(
        results,
        flush=True
    )

    # --------------------------------------------------------
    # EXTRACT RESULTS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # NO RESULTS
    # --------------------------------------------------------

    if not documents:

        print(
            "SEARCH STEP 5: No matching documents found",
            flush=True
        )

        print(
            "Possible reason:",
            flush=True
        )

        print(
            "The logged-in user_id does not match "
            "the user_id stored in ChromaDB.",
            flush=True
        )

        return []

    # --------------------------------------------------------
    # FORMAT RESULTS
    # --------------------------------------------------------

    search_results = []

    for index, text in enumerate(documents):

        metadata = metadatas[index]

        distance = float(
            distances[index]
        )

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

    # --------------------------------------------------------
    # CALCULATE RELEVANCE PERCENTAGE
    # --------------------------------------------------------

    distances_only = [

        result["distance"]

        for result in search_results

    ]

    min_distance = min(
        distances_only
    )

    max_distance = max(
        distances_only
    )

    for result in search_results:

        distance = result["distance"]

        if max_distance == min_distance:

            relevance_percentage = 100.0

        else:

            relevance_percentage = (

                (max_distance - distance)

                /

                (max_distance - min_distance)

            ) * 100

        relevance_percentage = max(
            0.0,
            min(
                100.0,
                relevance_percentage
            )
        )

        result[
            "relevance_percentage"
        ] = round(
            relevance_percentage,
            2
        )

    # --------------------------------------------------------
    # PRINT RESULTS
    # --------------------------------------------------------

    print(
        f"SEARCH STEP 5: Results found: "
        f"{len(search_results)}",
        flush=True
    )

    for result in search_results:

        print(
            "------------------------------------------",
            flush=True
        )

        print(
            "File:",
            result.get("file_name"),
            flush=True
        )

        print(
            "Chunk:",
            result.get("chunk_id"),
            flush=True
        )

        print(
            "User ID:",
            result.get("user_id"),
            flush=True
        )

        print(
            "Distance:",
            result.get("distance"),
            flush=True
        )

        print(
            "Relevance:",
            result.get(
                "relevance_percentage"
            ),
            flush=True
        )

        print(
            "Text:",
            result.get(
                "text",
                ""
            )[:200],
            flush=True
        )

    print(
        "------------------------------------------",
        flush=True
    )

    return search_results


# ============================================================
# DELETE DOCUMENT
# ============================================================

def delete_document(
    document_id
):

    if document_id is None:

        raise ValueError(
            "Document ID is required"
        )

    collection.delete(
        where={
            "document_id":
                str(document_id)
        }
    )

    return {

        "document_id":
            document_id,

        "deleted":
            True
    }


# ============================================================
# DELETE USER DOCUMENTS
# ============================================================

def delete_user_documents(
    user_id
):

    if user_id is None:

        raise ValueError(
            "User ID is required"
        )

    collection.delete(
        where={
            "user_id":
                str(user_id)
        }
    )

    return {

        "user_id":
            user_id,

        "deleted":
            True
    }


# ============================================================
# COLLECTION INFORMATION
# ============================================================

def get_collection_info():

    count = collection.count()

    return {

        "collection_name":
            COLLECTION_NAME,

        "collection_path":
            CHROMA_PATH,

        "total_chunks":
            count,

        "embedding_dimension":
            384,

        "distance_metric":
            "cosine"
    }
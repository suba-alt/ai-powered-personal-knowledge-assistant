from services.chroma_service import collection
from services.embedding_service import generate_embedding


# ============================================================
# SEARCH DOCUMENTS
# ============================================================

def search_documents(
    query,
    user_id,
    top_k=5
):

    # --------------------------------------------------------
    # VALIDATE QUERY
    # --------------------------------------------------------

    if not query or not query.strip():

        raise ValueError(
            "Search query cannot be empty"
        )

    query = query.strip()


    # --------------------------------------------------------
    # VALIDATE USER ID
    # --------------------------------------------------------

    if user_id is None:

        raise ValueError(
            "User ID is required"
        )


    # --------------------------------------------------------
    # GENERATE QUERY EMBEDDING
    # --------------------------------------------------------

    query_embedding = generate_embedding(
        query
    )


    # --------------------------------------------------------
    # LIMIT TOP K
    # --------------------------------------------------------

    top_k = max(
        1,
        int(top_k)
    )


    # --------------------------------------------------------
    # SEARCH CHROMADB
    # --------------------------------------------------------

    results = collection.query(

        query_embeddings=[
            query_embedding
        ],

        n_results=top_k,

        where={
            "user_id": str(user_id)
        },

        include=[
            "documents",
            "metadatas",
            "distances"
        ]

    )


    # --------------------------------------------------------
    # GET RESULTS
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

        return []


    # --------------------------------------------------------
    # BUILD SEARCH RESULTS
    # --------------------------------------------------------

    search_results = []


    for index, text in enumerate(
        documents
    ):

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


    # ========================================================
    # CALCULATE RELEVANCE PERCENTAGE
    # ========================================================

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


    # --------------------------------------------------------
    # CONVERT DISTANCE TO RELATIVE PERCENTAGE
    # --------------------------------------------------------

    for result in search_results:

        distance = result["distance"]


        if max_distance == min_distance:

            relevance_percentage = 100.0

        else:

            relevance_percentage = (

                (
                    max_distance - distance
                )

                /

                (
                    max_distance - min_distance
                )

            ) * 100


        # Keep value between 0 and 100

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
    # RETURN RESULTS
    # --------------------------------------------------------

    return search_results
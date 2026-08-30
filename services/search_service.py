from services.chroma_service import (
    search_documents as chroma_search
)


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

    # --------------------------------------------------------
    # SEARCH CHROMADB
    # --------------------------------------------------------

    results = chroma_search(
        question=query.strip(),
        user_id=user_id,
        top_k=top_k
    )

    return results
from flask import (
    Blueprint,
    request,
    jsonify
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from flasgger import swag_from

from services.chroma_service import (
    search_documents
)


# =========================================================
# SEARCH BLUEPRINT
# =========================================================

search_bp = Blueprint(
    "search",
    __name__
)


# =========================================================
# SEARCH DOCUMENTS
# POST /search
# =========================================================

@search_bp.route(
    "/search",
    methods=["POST"]
)
@jwt_required()
@swag_from({

    "tags": [
        "Search"
    ],

    "summary": "Search Documents",

    "description": (
        "Perform semantic search on the logged-in "
        "user's embedded documents using ChromaDB."
    ),

    "operationId": "searchDocuments",

    "consumes": [
        "application/json"
    ],

    "produces": [
        "application/json"
    ],

    "security": [
        {
            "Bearer": []
        }
    ],

    "parameters": [

        {
            "name": "body",

            "in": "body",

            "required": True,

            "schema": {

                "type": "object",

                "required": [
                    "query"
                ],

                "properties": {

                    "query": {

                        "type": "string",

                        "example":
                            "What is machine learning?"

                    },

                    "top_k": {

                        "type": "integer",

                        "example": 5,

                        "default": 5,

                        "description":
                            "Number of relevant chunks to return."

                    }

                }

            }

        }

    ],

    "responses": {

        "200": {

            "description":
                "Search completed successfully",

            "examples": {

                "application/json": {

                    "message":
                        "Search completed successfully",

                    "query":
                        "What is machine learning?",

                    "total_results":
                        2,

                    "results": [

                        {

                            "text":
                                "Machine learning is a branch of AI...",

                            "document_id":
                                "1",

                            "user_id":
                                "1",

                            "file_name":
                                "ai_notes.pdf",

                            "chunk_id":
                                "0",

                            "distance":
                                0.245

                        }

                    ]

                }

            }

        },

        "400": {

            "description":
                "Request body or query is missing"

        },

        "401": {

            "description":
                "Missing or invalid JWT token"

        },

        "500": {

            "description":
                "Search failed"

        }

    }

})
def search():

    # =====================================================
    # GET LOGGED-IN USER
    # =====================================================

    user_id = int(
        get_jwt_identity()
    )


    # =====================================================
    # GET REQUEST BODY
    # =====================================================

    data = request.get_json()


    if not data:

        return jsonify({

            "message":
                "Request body is required"

        }), 400


    # =====================================================
    # GET QUERY
    # =====================================================

    query = data.get(
        "query"
    )


    if not query:

        return jsonify({

            "message":
                "Query is required"

        }), 400


    # =====================================================
    # GET TOP K
    # =====================================================

    top_k = data.get(
        "top_k",
        5
    )


    try:

        top_k = int(
            top_k
        )

    except (TypeError, ValueError):

        return jsonify({

            "message":
                "top_k must be an integer"

        }), 400


    # =====================================================
    # VALIDATE TOP K
    # =====================================================

    if top_k <= 0:

        return jsonify({

            "message":
                "top_k must be greater than 0"

        }), 400


    # =====================================================
    # LIMIT RESULTS
    # =====================================================

    if top_k > 10:

        top_k = 10


    # =====================================================
    # CHROMADB SEMANTIC SEARCH
    # =====================================================

    try:

        results = search_documents(

            question=query,

            user_id=user_id,

            top_k=top_k

        )


        # =================================================
        # RESPONSE
        # =================================================

        return jsonify({

            "message":
                "Search completed successfully",

            "query":
                query,

            "total_results":
                len(results),

            "results":
                results

        }), 200


    except Exception as e:

        return jsonify({

            "message":
                "Search failed",

            "error":
                str(e)

        }), 500
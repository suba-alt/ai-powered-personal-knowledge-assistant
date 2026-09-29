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
# CREATE BLUEPRINT
# =========================================================

search_bp = Blueprint(
    "search",
    __name__
)


# =========================================================
# SEARCH API
# =========================================================

@search_bp.route(
    "/search",
    methods=["POST"]
)
@jwt_required()
@swag_from({
    "tags": ["Search"],
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
                "properties": {
                    "query": {
                        "type": "string",
                        "example": "What is Python?"
                    },
                    "top_k": {
                        "type": "integer",
                        "example": 5
                    }
                },
                "required": [
                    "query"
                ]
            }
        }
    ],
    "responses": {
        200: {
            "description": "Search completed successfully"
        },
        400: {
            "description": "Invalid request"
        },
        401: {
            "description": "Unauthorized"
        },
        500: {
            "description": "Search failed"
        }
    }
})
def search():

    # =====================================================
    # GET USER ID FROM JWT
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

    if not query or not query.strip():

        return jsonify({
            "message":
                "Query is required"
        }), 400

    query = query.strip()

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

    if top_k <= 0:

        return jsonify({
            "message":
                "top_k must be greater than 0"
        }), 400

    # Maximum 10 results

    if top_k > 10:

        top_k = 10

    # =====================================================
    # PERFORM SEMANTIC SEARCH
    # =====================================================

    try:

        print(
            "SEARCH API: Starting semantic search",
            flush=True
        )

        results = search_documents(
            question=query,
            user_id=user_id,
            top_k=top_k
        )

        print(
            f"SEARCH API: Results found = {len(results)}",
            flush=True
        )

        # =================================================
        # RETURN RESULTS
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

        print(
            "==========================================",
            flush=True
        )

        print(
            "SEARCH ERROR:",
            repr(e),
            flush=True
        )

        print(
            "==========================================",
            flush=True
        )

        return jsonify({

            "message":
                "Search failed",

            "error":
                str(e)

        }), 500
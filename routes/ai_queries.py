from flask import Blueprint, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from flasgger import swag_from

from model import AIQuery


ai_queries_bp = Blueprint(
    "ai_queries",
    __name__,
    url_prefix="/ai-queries"
)


# ============================================================
# GET AI QUERIES
# GET /ai-queries
# ============================================================

@ai_queries_bp.route(
    "",
    methods=["GET"]
)
@jwt_required()
@swag_from({
    "tags": [
        "AI Queries"
    ],

    "summary":
        "Get AI Queries",

    "description":
        "Get the AI questions asked by the logged-in user.",

    "security": [
        {
            "Bearer": []
        }
    ],

    "responses": {

        "200": {
            "description":
                "AI queries retrieved successfully"
        },

        "401": {
            "description":
                "Missing or invalid JWT token"
        },

        "500": {
            "description":
                "Failed to retrieve AI queries"
        }
    }
})
def get_ai_queries():

    try:

        user_id = get_jwt_identity()

        queries = AIQuery.query.filter_by(
            user_id=user_id
        ).order_by(
            AIQuery.created_at.desc()
        ).all()

        result = []

        for query in queries:

            result.append({

                "id":
                    query.id,

                "user_id":
                    query.user_id,

                "question":
                    query.question,

                "created_at":
                    query.created_at.isoformat()
                    if query.created_at
                    else None

            })

        return jsonify({

            "message":
                "AI queries retrieved successfully",

            "queries":
                result

        }), 200

    except Exception as e:

        return jsonify({

            "message":
                "Failed to retrieve AI queries",

            "error":
                str(e)

        }), 500
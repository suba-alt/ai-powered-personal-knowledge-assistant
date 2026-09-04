from flask import Blueprint, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from flasgger import swag_from

from db import db
from model import AIQuery, ChatHistory


chat_history_bp = Blueprint(
    "chat_history",
    __name__,
    url_prefix="/chat-history"
)


# ============================================================
# GET CHAT HISTORY
# GET /chat-history
# ============================================================

@chat_history_bp.route(
    "",
    methods=["GET"]
)
@jwt_required()
@swag_from({
    "tags": [
        "Chat History"
    ],

    "summary":
        "Get Chat History",

    "description":
        "Get the AI chat history of the logged-in user.",

    "security": [
        {
            "Bearer": []
        }
    ],

    "responses": {

        "200": {
            "description":
                "Chat history retrieved successfully"
        },

        "401": {
            "description":
                "Missing or invalid JWT token"
        },

        "500": {
            "description":
                "Failed to retrieve chat history"
        }
    }
})
def get_chat_history():

    try:

        user_id = get_jwt_identity()

        history = (
            db.session.query(ChatHistory, AIQuery)
            .join(
                AIQuery,
                ChatHistory.query_id == AIQuery.id
            )
            .filter(
                AIQuery.user_id == user_id
            )
            .order_by(
                ChatHistory.created_at.desc()
            )
            .all()
        )

        result = []

        for chat, query in history:

            result.append({

                "id":
                    chat.id,

                "query_id":
                    chat.query_id,

                "question":
                    query.question
                    if query
                    else None,

                "ai_response":
                    chat.ai_response,

                "confidence_score":
                    float(chat.confidence_score)
                    if chat.confidence_score is not None
                    else None,

                "created_at":
                    chat.created_at.isoformat()
                    if chat.created_at
                    else None
            })

        return jsonify({

            "message":
                "Chat history retrieved successfully",

            "history":
                result

        }), 200

    except Exception as e:

        return jsonify({

            "message":
                "Failed to retrieve chat history",

            "error":
                str(e)

        }), 500
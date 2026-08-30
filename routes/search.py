from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

search_bp = Blueprint(
    "search",
    __name__
)


@search_bp.route(
    "/search",
    methods=["POST"]
)
@jwt_required()
def search():

    data = request.get_json()

    if not data:

        return jsonify({
            "message": "Request body is required"
        }), 400

    query = data.get("query")

    if not query:

        return jsonify({
            "message": "Query is required"
        }), 400

    # Your ChromaDB search code goes here

    return jsonify({
        "message": "Search endpoint is working",
        "query": query
    }), 200
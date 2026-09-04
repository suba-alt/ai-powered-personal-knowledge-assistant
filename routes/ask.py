from flask import (
    Blueprint,
    request,
    jsonify
)

from model import AIQuery, ChatHistory
from db import db

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from flasgger import swag_from

from services.search_service import (
    search_documents
)

from services.llm_service import (
    generate_answer
)


# ============================================================
# BLUEPRINT
# ============================================================

ask_bp = Blueprint(
    "ask",
    __name__,
    url_prefix="/ask"
)


# ============================================================
# ASK QUESTION
# POST /ask
# ============================================================

@ask_bp.route(
    "",
    methods=["POST"]
)
@jwt_required()
@swag_from({
    "tags": [
        "Ask"
    ],

    "summary":
        "Ask Question",

    "description":
        "Ask a question and generate an AI answer "
        "using relevant information from the user's "
        "uploaded documents. The question and AI response "
        "are stored in the AI query and chat history tables.",

    "operationId":
        "askQuestion",

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
            "name":
                "body",

            "in":
                "body",

            "required":
                True,

            "description":
                "Question to ask the AI.",

            "schema": {
                "type":
                    "object",

                "required": [
                    "query"
                ],

                "properties": {

                    "query": {
                        "type":
                            "string",

                        "description":
                            "Question to ask.",

                        "example":
                            "What is machine learning?"
                    },

                    "top_k": {
                        "type":
                            "integer",

                        "description":
                            "Number of relevant document chunks "
                            "to retrieve.",

                        "default":
                            5,

                        "example":
                            5
                    }
                }
            }
        }
    ],

    "responses": {

        "200": {
            "description":
                "Question answered successfully",

            "examples": {
                "application/json": {

                    "message":
                        "Question answered successfully",

                    "query":
                        "What is machine learning?",

                    "answer":
                        "Machine learning is a method of "
                        "teaching computers to learn from data.",

                    "confidence_score":
                        87.50,

                    "sources": [
                        {
                            "text":
                                "Machine learning is a branch "
                                "of artificial intelligence...",

                            "document_id":
                                "1",

                            "user_id":
                                "1",

                            "file_name":
                                "AI_Notes.pdf",

                            "chunk_id":
                                "0",

                            "distance":
                                0.125,

                            "relevance_percentage":
                                100.0
                        }
                    ]
                }
            }
        },

        "400": {
            "description":
                "Invalid request"
        },

        "401": {
            "description":
                "Missing or invalid JWT token"
        },

        "500": {
            "description":
                "Question answering failed"
        }
    }
})
def ask():

    try:

        # ----------------------------------------------------
        # GET LOGGED-IN USER
        # ----------------------------------------------------

        user_id = get_jwt_identity()


        # ----------------------------------------------------
        # GET JSON REQUEST
        # ----------------------------------------------------

        data = request.get_json(
            silent=True
        )


        if not data:

            return jsonify({

                "message":
                    "Request body is required"

            }), 400


        # ----------------------------------------------------
        # GET QUESTION
        # ----------------------------------------------------

        question = data.get(
            "query"
        )


        if question is None:

            return jsonify({

                "message":
                    "Query is required"

            }), 400


        question = str(
            question
        ).strip()


        if not question:

            return jsonify({

                "message":
                    "Query cannot be empty"

            }), 400


        # ----------------------------------------------------
        # GET TOP K
        # ----------------------------------------------------

        top_k = data.get(
            "top_k",
            5
        )


        try:

            top_k = int(
                top_k
            )

        except (
            TypeError,
            ValueError
        ):

            return jsonify({

                "message":
                    "top_k must be an integer"

            }), 400


        # ----------------------------------------------------
        # VALIDATE TOP K
        # ----------------------------------------------------

        if top_k <= 0:

            return jsonify({

                "message":
                    "top_k must be greater than 0"

            }), 400


        # ----------------------------------------------------
        # LIMIT TOP K
        # ----------------------------------------------------

        if top_k > 10:

            top_k = 10


        # ----------------------------------------------------
        # SEARCH CHROMADB
        # ----------------------------------------------------

        search_results = search_documents(

            query=question,

            user_id=user_id,

            top_k=top_k

        )


        # ----------------------------------------------------
        # CHECK SEARCH RESULTS
        # ----------------------------------------------------

        if not search_results:

            return jsonify({

                "message":
                    "No relevant information found",

                "query":
                    question,

                "answer":
                    "I could not find this information "
                    "in your documents.",

                "confidence_score":
                    0.00,

                "sources":
                    []

            }), 200


        # ----------------------------------------------------
        # BUILD DOCUMENT CONTEXT
        # ----------------------------------------------------

        context_parts = []


        for result in search_results:

            text = result.get(
                "text"
            )


            if text:

                context_parts.append(
                    text
                )


        context = "\n\n".join(
            context_parts
        )


        # ----------------------------------------------------
        # CHECK CONTEXT
        # ----------------------------------------------------

        if not context.strip():

            return jsonify({

                "message":
                    "No usable document context found",

                "query":
                    question,

                "answer":
                    "I could not find enough information "
                    "in your documents.",

                "confidence_score":
                    0.00,

                "sources":
                    search_results

            }), 200


        # ----------------------------------------------------
        # GENERATE AI ANSWER
        # ----------------------------------------------------

        answer = generate_answer(

            question=question,

            context=context

        )


        # ====================================================
        # CALCULATE CONFIDENCE SCORE
        # ====================================================
        #
        # search_service.py already calculates:
        #
        # relevance_percentage
        #
        # Therefore, use that value instead of converting
        # ChromaDB distance directly.
        #
        # This gives us a retrieval/context relevance score.
        # ====================================================

        relevance_scores = []


        for result in search_results:

            relevance = result.get(
                "relevance_percentage"
            )


            if relevance is not None:

                try:

                    relevance_scores.append(
                        float(relevance)
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    pass


        if relevance_scores:

            confidence_score = (
                sum(relevance_scores)
                /
                len(relevance_scores)
            )

        else:

            confidence_score = 0.00


        # ----------------------------------------------------
        # KEEP SCORE BETWEEN 0 AND 100
        # ----------------------------------------------------

        confidence_score = max(
            0.00,
            min(
                100.00,
                confidence_score
            )
        )


        confidence_score = round(
            confidence_score,
            2
        )


        # ----------------------------------------------------
        # SAVE AI QUERY
        # ----------------------------------------------------

        ai_query = AIQuery(

            user_id=user_id,

            question=question

        )


        db.session.add(
            ai_query
        )


        # ----------------------------------------------------
        # GET GENERATED QUERY ID
        # ----------------------------------------------------

        db.session.flush()


        # ----------------------------------------------------
        # SAVE CHAT HISTORY
        # ----------------------------------------------------

        chat_history = ChatHistory(

            query_id=ai_query.id,

            ai_response=answer,

            confidence_score=confidence_score

        )


        db.session.add(
            chat_history
        )


        # ----------------------------------------------------
        # COMMIT DATABASE CHANGES
        # ----------------------------------------------------

        db.session.commit()


        # ----------------------------------------------------
        # RETURN RESPONSE
        # ----------------------------------------------------

        return jsonify({

            "message":
                "Question answered successfully",

            "query":
                question,

            "answer":
                answer,

            "confidence_score":
                confidence_score,

            "sources":
                search_results

        }), 200


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except ValueError as e:

        db.session.rollback()

        return jsonify({

            "message":
                str(e)

        }), 400


    except Exception as e:

        db.session.rollback()

        return jsonify({

            "message":
                "Question answering failed",

            "error":
                str(e)

        }), 500
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

from services.chroma_service import (
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
        "uploaded documents.",

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
                            "What is software testing?"
                    },

                    "top_k": {

                        "type":
                            "integer",

                        "description":
                            "Number of relevant document "
                            "chunks to retrieve.",

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
                "Question answered successfully"
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

        # ====================================================
        # STEP 1 — GET LOGGED-IN USER
        # ====================================================

        user_id = get_jwt_identity()

        print(
            "==========================================",
            flush=True
        )

        print(
            "ASK API: User ID =",
            user_id,
            flush=True
        )

        print(
            "ASK API: User ID type =",
            type(user_id),
            flush=True
        )

        if user_id is None:

            return jsonify({

                "message":
                    "User identity not found"

            }), 401

        # ====================================================
        # STEP 2 — GET REQUEST BODY
        # ====================================================

        data = request.get_json(
            silent=True
        )

        if not data:

            return jsonify({

                "message":
                    "Request body is required"

            }), 400

        # ====================================================
        # STEP 3 — GET QUESTION
        # ====================================================

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

        # ====================================================
        # STEP 4 — GET TOP K
        # ====================================================

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

        # ====================================================
        # STEP 5 — VALIDATE TOP K
        # ====================================================

        if top_k <= 0:

            return jsonify({

                "message":
                    "top_k must be greater than 0"

            }), 400

        if top_k > 10:

            top_k = 10

        # ====================================================
        # STEP 6 — SEMANTIC SEARCH
        # ====================================================

        print(
            "ASK STEP 1: Starting semantic search",
            flush=True
        )

        search_results = search_documents(

            question=question,

            user_id=user_id,

            top_k=top_k
        )

        print(
            f"ASK STEP 2: Search results = "
            f"{len(search_results)}",
            flush=True
        )

        # ====================================================
        # DEBUG SEARCH RESULTS
        # ====================================================

        for index, result in enumerate(
            search_results,
            start=1
        ):

            print(
                f"ASK SEARCH RESULT {index}:",
                flush=True
            )

            print(
                "  File:",
                result.get("file_name"),
                flush=True
            )

            print(
                "  Chunk:",
                result.get("chunk_id"),
                flush=True
            )

            print(
                "  Distance:",
                result.get("distance"),
                flush=True
            )

            print(
                "  Relevance:",
                result.get(
                    "relevance_percentage"
                ),
                flush=True
            )

            print(
                "  Text preview:",
                result.get(
                    "text",
                    ""
                )[:300],
                flush=True
            )

        # ====================================================
        # STEP 7 — NO SEARCH RESULTS
        # ====================================================

        if not search_results:

            print(
                "ASK STEP 3: No relevant chunks found",
                flush=True
            )

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

        # ====================================================
        # STEP 8 — BUILD RAG CONTEXT
        # ====================================================

        context_parts = []

        for index, result in enumerate(
            search_results,
            start=1
        ):

            text = result.get(
                "text",
                ""
            )

            file_name = result.get(
                "file_name",
                "Unknown file"
            )

            chunk_id = result.get(
                "chunk_id",
                "Unknown chunk"
            )

            if text and text.strip():

                context_parts.append(

                    f"""
SOURCE {index}

FILE:
{file_name}

CHUNK:
{chunk_id}

CONTENT:
{text.strip()}
"""
                )

        context = "\n\n".join(
            context_parts
        )

        print(
            f"ASK STEP 3: Context chunks = "
            f"{len(context_parts)}",
            flush=True
        )

        # ====================================================
        # STEP 9 — CHECK CONTEXT
        # ====================================================

        if not context.strip():

            print(
                "ASK STEP 4: Context is empty",
                flush=True
            )

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

        # ====================================================
        # STEP 10 — CONTEXT DEBUG
        # ====================================================

        print(
            f"ASK STEP 4: Context length = "
            f"{len(context)} characters",
            flush=True
        )

        print(
            "ASK STEP 4: Context preview:",
            flush=True
        )

        print(
            context[:2000],
            flush=True
        )

        # ====================================================
        # STEP 11 — GENERATE GEMINI ANSWER
        # ====================================================

        print(
            "ASK STEP 5: Generating Gemini answer",
            flush=True
        )

        answer = generate_answer(

            question=question,

            context=context
        )

        print(
            "ASK STEP 6: Gemini answer generated",
            flush=True
        )

        print(
            "ASK ANSWER:",
            answer,
            flush=True
        )

        # ====================================================
        # STEP 12 — CALCULATE CONFIDENCE SCORE
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

                sum(
                    relevance_scores
                )

                /

                len(
                    relevance_scores
                )
            )

        else:

            confidence_score = 0.00

        # ====================================================
        # LIMIT SCORE
        # ====================================================

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

        print(
            "ASK CONFIDENCE SCORE:",
            confidence_score,
            flush=True
        )

        # ====================================================
        # STEP 13 — SAVE AI QUERY
        # ====================================================

        ai_query = AIQuery(

            user_id=user_id,

            question=question
        )

        db.session.add(
            ai_query
        )

        # ====================================================
        # STEP 14 — GENERATE QUERY ID
        # ====================================================

        db.session.flush()

        print(
            "ASK QUERY ID:",
            ai_query.id,
            flush=True
        )

        # ====================================================
        # STEP 15 — SAVE CHAT HISTORY
        # ====================================================

        chat_history = ChatHistory(

            query_id=ai_query.id,

            ai_response=answer,

            confidence_score=confidence_score
        )

        db.session.add(
            chat_history
        )

        # ====================================================
        # STEP 16 — COMMIT DATABASE
        # ====================================================

        db.session.commit()

        print(
            f"ASK STEP 7: Saved query ID = "
            f"{ai_query.id}",
            flush=True
        )

        print(
            "==========================================",
            flush=True
        )

        # ====================================================
        # STEP 17 — RETURN RESPONSE
        # ====================================================

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
    # VALUE ERROR
    # ========================================================

    except ValueError as e:

        db.session.rollback()

        print(
            "==========================================",
            flush=True
        )

        print(
            "ASK VALUE ERROR:",
            repr(e),
            flush=True
        )

        print(
            "==========================================",
            flush=True
        )

        return jsonify({

            "message":
                str(e)

        }), 400

    # ========================================================
    # GENERAL ERROR
    # ========================================================

    except Exception as e:

        db.session.rollback()

        print(
            "==========================================",
            flush=True
        )

        print(
            "ASK ERROR:",
            repr(e),
            flush=True
        )

        print(
            "==========================================",
            flush=True
        )

        return jsonify({

            "message":
                "Question answering failed",

            "error":
                str(e)

        }), 500
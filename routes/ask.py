from flask import (
    Blueprint,
    request,
    jsonify
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

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
        # SEARCH CHROMADB
        # ----------------------------------------------------

        search_results = search_documents(

            query=question,

            user_id=user_id,

            top_k=5

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
                    "I could not find this information in your documents.",

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
                    "I could not find enough information in your documents.",

                "sources":
                    search_results

            }), 200


        # ----------------------------------------------------
        # GENERATE GEMINI ANSWER
        # ----------------------------------------------------

        answer = generate_answer(

            question=question,

            context=context

        )


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

            "sources":
                search_results

        }), 200


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except ValueError as e:

        return jsonify({

            "message":
                str(e)

        }), 400


    except Exception as e:

        return jsonify({

            "message":
                "Question answering failed",

            "error":
                str(e)

        }), 500
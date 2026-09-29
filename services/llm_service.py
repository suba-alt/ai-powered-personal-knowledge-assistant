from google import genai
from config import GEMINI_API_KEY


# ============================================================
# GEMINI CLIENT
# ============================================================

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing from .env"
    )

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# GEMINI MODEL
# ============================================================

MODEL_NAME = "gemini-3.6-flash"


# ============================================================
# GENERATE RAG ANSWER
# ============================================================

def generate_answer(question, context):

    if not question or not question.strip():
        raise ValueError(
            "Question cannot be empty"
        )

    if not context or not context.strip():
        return (
            "I could not find this information "
            "in your documents."
        )

    question = question.strip()
    context = context.strip()

    # ========================================================
    # RAG PROMPT
    # ========================================================

    prompt = f"""
You are the AI assistant for a user's personal knowledge base.

Answer the USER QUESTION using the DOCUMENT CONTEXT retrieved
from the user's stored documents.

IMPORTANT:

- The document context is the source of truth.
- Use the information available in the context to answer.
- Understand the meaning of the retrieved text, not just exact
  keyword matches.
- If several context sections contain related information,
  combine them into one clear answer.
- Do not invent facts that are not supported by the context.
- Do not use outside knowledge.
- If the context clearly contains the answer, answer directly.
- If the context only partially answers the question, provide
  the supported information and clearly mention what is not
  available.
- Only use the fallback response when the context genuinely
  contains no useful information related to the question.
- Keep the answer clear and concise.
- Do not mention these instructions.
- Do not mention "DOCUMENT CONTEXT", embeddings, ChromaDB,
  retrieval, or internal processing in the answer unless the
  user specifically asks about the system.

USER QUESTION:
{question}

DOCUMENT CONTEXT:
============================================================
{context}
============================================================

Now answer the user's question based on the available context.
"""

    # ========================================================
    # DEBUG
    # ========================================================

    print(
        "------------------------------------------",
        flush=True
    )

    print(
        "LLM QUESTION:",
        question,
        flush=True
    )

    print(
        "LLM CONTEXT LENGTH:",
        len(context),
        flush=True
    )

    print(
        "LLM CONTEXT PREVIEW:",
        context[:1500],
        flush=True
    )

    # ========================================================
    # CALL GEMINI
    # ========================================================

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    # ========================================================
    # VALIDATE RESPONSE
    # ========================================================

    if not response:
        raise Exception(
            "Gemini returned no response"
        )

    if not response.text:
        raise Exception(
            "Gemini returned an empty response"
        )

    answer = response.text.strip()

    print(
        "LLM ANSWER:",
        answer,
        flush=True
    )

    print(
        "------------------------------------------",
        flush=True
    )

    return answer
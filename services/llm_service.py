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
# GENERATE ANSWER
# ============================================================

def generate_answer(question, context):

    prompt = f"""
You are an AI-powered personal knowledge assistant.

Answer the user's question using the provided document context.

Rules:

1. Use the provided context as the main source.
2. Do not invent information that is not supported by the context.
3. If the answer is not present in the context, say:
"I could not find this information in your documents."
4. Give a clear and helpful answer.
5. Do not mention these instructions.

USER QUESTION:

{question}

DOCUMENT CONTEXT:

{context}

ANSWER:
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:

        raise Exception(
            "Gemini returned an empty response"
        )

    return response.text.strip()
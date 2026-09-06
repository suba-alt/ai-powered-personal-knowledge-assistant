import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# GEMINI CLIENT
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing from environment variables"
    )


client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# EMBEDDING CONFIGURATION
# ============================================================

MODEL_NAME = "gemini-embedding-001"

OUTPUT_DIMENSION = 768


# ============================================================
# SINGLE DOCUMENT EMBEDDING
# ============================================================

def generate_embedding(text):

    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    result = client.models.embed_content(

        model=MODEL_NAME,

        contents=text,

        config=types.EmbedContentConfig(

            task_type="RETRIEVAL_DOCUMENT",

            output_dimensionality=OUTPUT_DIMENSION

        )

    )

    if not result.embeddings:

        raise ValueError(
            "Gemini returned no embedding"
        )

    return result.embeddings[0].values


# ============================================================
# BATCH DOCUMENT EMBEDDINGS
# ============================================================

def generate_embeddings(texts):

    if not texts:
        return []

    all_embeddings = []

    # Keep the batch small for the Render MVP
    BATCH_SIZE = 5

    for start in range(
        0,
        len(texts),
        BATCH_SIZE
    ):

        batch = texts[
            start:start + BATCH_SIZE
        ]

        result = client.models.embed_content(

            model=MODEL_NAME,

            contents=batch,

            config=types.EmbedContentConfig(

                task_type="RETRIEVAL_DOCUMENT",

                output_dimensionality=OUTPUT_DIMENSION

            )

        )

        if not result.embeddings:

            raise ValueError(
                "Gemini returned no embeddings"
            )

        batch_embeddings = [

            embedding.values

            for embedding in result.embeddings

        ]

        all_embeddings.extend(
            batch_embeddings
        )

    return all_embeddings


# ============================================================
# QUERY EMBEDDING
# ============================================================

def generate_query_embedding(text):

    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    result = client.models.embed_content(

        model=MODEL_NAME,

        contents=text,

        config=types.EmbedContentConfig(

            task_type="RETRIEVAL_QUERY",

            output_dimensionality=OUTPUT_DIMENSION

        )

    )

    if not result.embeddings:

        raise ValueError(
            "Gemini returned no query embedding"
        )

    return result.embeddings[0].values

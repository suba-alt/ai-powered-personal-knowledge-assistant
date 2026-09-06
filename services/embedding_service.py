import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

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

    return result.embeddings[0].values


# ============================================================
# BATCH DOCUMENT EMBEDDINGS
# ============================================================

def generate_embeddings(texts):

    if not texts:
        return []

    all_embeddings = []

    BATCH_SIZE = 10

    for start in range(0, len(texts), BATCH_SIZE):

        batch = texts[start:start + BATCH_SIZE]

        result = client.models.embed_content(
            model=MODEL_NAME,
            contents=batch,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=OUTPUT_DIMENSION
            )
        )

        batch_embeddings = [
            embedding.values
            for embedding in result.embeddings
        ]

        all_embeddings.extend(batch_embeddings)

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

    return result.embeddings[0].values
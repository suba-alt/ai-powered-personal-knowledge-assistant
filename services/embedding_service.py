import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL_NAME = "gemini-embedding-001"

# Smaller vectors = less Chroma storage
OUTPUT_DIMENSION = 768


# ==========================================
# SINGLE DOCUMENT EMBEDDING
# ==========================================

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


# ==========================================
# BATCH DOCUMENT EMBEDDINGS
# ==========================================

def generate_embeddings(texts):

    if not texts:
        return []

    result = client.models.embed_content(
        model=MODEL_NAME,
        contents=texts,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=OUTPUT_DIMENSION
        )
    )

    return [
        embedding.values
        for embedding in result.embeddings
    ]


# ==========================================
# QUERY EMBEDDING
# ==========================================

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
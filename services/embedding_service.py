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


def generate_embeddings(texts):
    if not texts:
        return []

    all_embeddings = []

    for text in texts:
        if not text or not text.strip():
            continue

        result = client.models.embed_content(
            model=MODEL_NAME,
            contents=text,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=OUTPUT_DIMENSION
            )
        )

        if not result.embeddings:
            raise ValueError("Gemini returned no embedding")

        all_embeddings.append(
            result.embeddings[0].values
        )

    return all_embeddings


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

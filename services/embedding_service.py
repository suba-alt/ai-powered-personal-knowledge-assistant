from sentence_transformers import SentenceTransformer


# ============================================================
# MODEL CONFIGURATION
# ============================================================

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Load model only once when Flask starts
model = SentenceTransformer(MODEL_NAME)


# ============================================================
# GENERATE SINGLE EMBEDDING
# ============================================================

def generate_embedding(text):

    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()


# ============================================================
# GENERATE MULTIPLE EMBEDDINGS
# ============================================================

def generate_embeddings(texts):

    if not texts:
        return []

    valid_texts = [
        text.strip()
        for text in texts
        if text and text.strip()
    ]

    if not valid_texts:
        return []

    embeddings = model.encode(
        valid_texts,
        normalize_embeddings=True
    )

    return embeddings.tolist()


# ============================================================
# GENERATE QUERY EMBEDDING
# ============================================================

def generate_query_embedding(text):

    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()

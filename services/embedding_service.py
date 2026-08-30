from sentence_transformers import SentenceTransformer


# ==========================================
# EMBEDDING MODEL
# ==========================================

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


model = SentenceTransformer(
    MODEL_NAME
)


# ==========================================
# SINGLE TEXT EMBEDDING
# ==========================================

def generate_embedding(text):

    if not text or not text.strip():

        raise ValueError(
            "Text cannot be empty"
        )

    embedding = model.encode(
        text,
        convert_to_numpy=True
    )

    return embedding.tolist()


# ==========================================
# MULTIPLE TEXT EMBEDDINGS
# ==========================================

def generate_embeddings(texts):

    if not texts:

        return []

    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    )

    return embeddings.tolist()
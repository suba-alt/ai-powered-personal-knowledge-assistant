from sentence_transformers import SentenceTransformer


# ==========================================
# EMBEDDING MODEL
# ==========================================

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(
    MODEL_NAME,
    device="cpu"
)

# Reduce maximum sequence length to reduce memory usage
model.max_seq_length = 256


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
        convert_to_numpy=True,
        batch_size=1,
        show_progress_bar=False
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
        convert_to_numpy=True,
        batch_size=8,
        show_progress_bar=False
    )

    return embeddings.tolist()
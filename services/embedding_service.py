from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = None


def get_model():

    global model

    if model is None:

        model = SentenceTransformer(
            MODEL_NAME,
            device="cpu"
        )

        model.max_seq_length = 256

    return model


def generate_embedding(text):

    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    embedding = get_model().encode(
        text,
        convert_to_numpy=True,
        batch_size=1,
        show_progress_bar=False
    )

    return embedding.tolist()


def generate_embeddings(texts):

    if not texts:
        return []

    embeddings = get_model().encode(
        texts,
        convert_to_numpy=True,
        batch_size=8,
        show_progress_bar=False
    )

    return embeddings.tolist()
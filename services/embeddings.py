import os

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer


load_dotenv()


MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2"
)


_embedding_model = None


def get_embedding_model():

    global _embedding_model

    if _embedding_model is None:

        _embedding_model = SentenceTransformer(
            MODEL_NAME
        )

    return _embedding_model


def create_embeddings(texts):

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    return embeddings.tolist()

from sentence_transformers import SentenceTransformer
from functools import lru_cache
from typing import List, Union

# -----------------------------
# Load Model (cached, lazy)
# -----------------------------
@lru_cache(maxsize=1)
def get_model():
    """
    Loads the embedding model only once (singleton pattern).
    Prevents reloading on every request.
    """
    return SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# Generate Embedding (single)
# -----------------------------
def get_embedding(text: str) -> List[float]:
    """
    Convert text → embedding vector
    """
    model = get_model()

    embedding = model.encode(
        text,
        normalize_embeddings=True  # cosine similarity optimization
    )

    return embedding.tolist()


# -----------------------------
# Generate Embeddings (batch)
# -----------------------------
def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Batch embedding generation (faster for seeding / bulk ops)
    """
    model = get_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        batch_size=32,
        show_progress_bar=False
    )

    return [emb.tolist() for emb in embeddings]
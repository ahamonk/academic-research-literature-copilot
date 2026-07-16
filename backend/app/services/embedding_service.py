import os

os.environ.setdefault("HF_HUB_OFFLINE", "1")

MODEL_NAME = "all-MiniLM-L6-v2"

_model = None


def _get_model():
    """
    Lazily import sentence-transformers and load the model on first use.
    HF_HUB_OFFLINE=1 (set above) stops huggingface_hub from making a
    network call to check for model updates on load — since the model
    was already downloaded and cached locally in Day 2, this avoids a
    potentially slow/hanging network check on every first use.
    """
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def generate_embedding(text: str) -> list[float]:
    """Generate a single embedding vector for one piece of text."""
    model = _get_model()
    return model.encode(text).tolist()


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Generate embedding vectors for a batch of texts (more efficient than one-by-one)."""
    model = _get_model()
    return model.encode(texts).tolist()
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    """
    Lazily load the model once and reuse it across requests.
    Avoids reloading the model (slow, memory-heavy) on every call.
    """
    global _model
    if _model is None:
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
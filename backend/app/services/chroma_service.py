import chromadb

CHROMA_PERSIST_DIR = "chroma_db"
COLLECTION_NAME = "papers"

_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
_collection = _client.get_or_create_collection(name=COLLECTION_NAME)


def add_papers_to_chroma(papers: list[dict], embeddings: list[list[float]]) -> None:
    """
    Store paper embeddings in ChromaDB.
    Each paper dict must contain: arxiv_id, abstract, title, authors,
    primary_category, published_date, arxiv_url.
    """
    if not papers:
        return

    ids = [p["arxiv_id"] for p in papers]
    documents = [p["abstract"] for p in papers]
    metadatas = [
        {
            "title": p["title"],
            "authors": p["authors"],
            "primary_category": p["primary_category"],
            "published_date": str(p["published_date"]),
            "arxiv_url": p["arxiv_url"],
        }
        for p in papers
    ]

    _collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def query_similar_papers(query_embedding: list[float], top_k: int) -> dict:
    """
    Query ChromaDB for the papers most similar to the given embedding.
    Returns Chroma's raw result dict, containing 'ids' and 'distances'
    (each a list-of-lists, one inner list per query embedding — we only
    ever send one, so callers should index [0]).
    """
    return _collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )


def get_collection():
    """Expose the collection for inspection/debugging."""
    return _collection
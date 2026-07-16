import chromadb

CHROMA_PERSIST_DIR = "chroma_db"
COLLECTION_NAME = "papers"

_client = None
_collection = None


def _get_collection():
    """
    Lazily create the ChromaDB client and collection on first use, rather
    than at module import time. Matches the lazy-loading pattern already
    used for the SentenceTransformer model in embedding_service.py, and
    keeps app startup from paying this cost unconditionally.
    """
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        _collection = _client.get_or_create_collection(name=COLLECTION_NAME)
    return _collection


def add_papers_to_chroma(papers: list[dict], embeddings: list[list[float]]) -> None:
    """
    Store paper embeddings in ChromaDB.
    Each paper dict must contain: arxiv_id, abstract, title, authors,
    primary_category, published_date, arxiv_url.
    """
    if not papers:
        return

    collection = _get_collection()

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

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def query_similar_papers(query_embedding: list[float], top_k: int) -> dict:
    """
    Query ChromaDB for the papers most similar to the given embedding.
    """
    collection = _get_collection()
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )


def get_all_embeddings() -> tuple[list[str], list[list[float]]]:
    """
    Retrieve every stored paper's arxiv_id and embedding vector from
    ChromaDB, in matching order. Used by the clustering pipeline.
    """
    collection = _get_collection()
    result = collection.get(include=["embeddings"])
    ids = result["ids"] or []
    raw_embeddings = result["embeddings"]

    if raw_embeddings is None:
        embeddings = []
    else:
        embeddings = [list(vector) for vector in raw_embeddings]

    return ids, embeddings


def get_collection():
    """Expose the collection for inspection/debugging."""
    return _get_collection()
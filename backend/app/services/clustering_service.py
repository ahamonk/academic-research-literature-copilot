import numpy as np
from sqlalchemy.orm import Session

from app.models.paper import Paper
from app.services.chroma_service import get_all_embeddings
from app.services.dimensionality_service import reduce_to_2d


def run_hdbscan(embeddings: list[list[float]], min_cluster_size: int = 2) -> list[int]:
    """
    Run HDBSCAN on a list of embedding vectors.
    Returns cluster labels in the same order as the input; -1 means noise
    (a paper that didn't fit cleanly into any cluster).

    hdbscan is imported here, not at module level, because it (via numba)
    has a heavy one-time JIT compilation cost on import. Deferring the
    import until clustering is actually needed keeps app startup fast.
    """
    import hdbscan

    if not embeddings:
        return []

    embeddings_array = np.array(embeddings)
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size)
    labels = clusterer.fit_predict(embeddings_array)

    return [int(label) for label in labels]


def get_clustered_papers(db: Session, min_cluster_size: int = 2) -> list[dict]:
    """
    Retrieve all paper embeddings from ChromaDB, run HDBSCAN, and combine
    the resulting cluster assignments with full paper metadata from
    PostgreSQL (looked up by arxiv_id).
    """
    ids, embeddings = get_all_embeddings()
    if not ids:
        return []

    labels = run_hdbscan(embeddings, min_cluster_size=min_cluster_size)

    papers = db.query(Paper).filter(Paper.arxiv_id.in_(ids)).all()
    papers_by_id = {p.arxiv_id: p for p in papers}

    results = []
    for arxiv_id, label in zip(ids, labels):
        paper = papers_by_id.get(arxiv_id)
        if paper is None:
            continue
        results.append(
            {
                "arxiv_id": paper.arxiv_id,
                "title": paper.title,
                "authors": paper.authors,
                "abstract": paper.abstract,
                "primary_category": paper.primary_category,
                "published_date": paper.published_date,
                "arxiv_url": paper.arxiv_url,
                "cluster_id": label,
            }
        )
    return results


def get_clustered_papers_with_coordinates(db: Session, min_cluster_size: int = 2) -> list[dict]:
    """
    Same as get_clustered_papers(), but also runs UMAP on the same
    embeddings to produce 2D (x, y) coordinates for visualization.
    cluster_id, x, and y all come from the same embedding set, so they
    stay consistent with each other.
    """
    ids, embeddings = get_all_embeddings()
    if not ids:
        return []

    labels = run_hdbscan(embeddings, min_cluster_size=min_cluster_size)
    coordinates = reduce_to_2d(embeddings)

    papers = db.query(Paper).filter(Paper.arxiv_id.in_(ids)).all()
    papers_by_id = {p.arxiv_id: p for p in papers}

    results = []
    for arxiv_id, label, (x, y) in zip(ids, labels, coordinates):
        paper = papers_by_id.get(arxiv_id)
        if paper is None:
            continue
        results.append(
            {
                "arxiv_id": paper.arxiv_id,
                "title": paper.title,
                "authors": paper.authors,
                "abstract": paper.abstract,
                "primary_category": paper.primary_category,
                "published_date": paper.published_date,
                "arxiv_url": paper.arxiv_url,
                "cluster_id": label,
                "x": x,
                "y": y,
            }
        )
    return results
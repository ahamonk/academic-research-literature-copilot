import numpy as np
from sqlalchemy.orm import Session

from app.models.paper import Paper
from app.services.chroma_service import get_all_embeddings
from app.services.dimensionality_service import reduce_to_2d

CANDIDATE_K_VALUES = [4, 6, 8, 10, 12]


def _select_best_k(embeddings_array: np.ndarray) -> int:
    """
    Evaluate each candidate K (that's actually valid for the current
    dataset size) using the Silhouette Score, and return the K with the
    highest score. Falls back to a small, safe K if there isn't enough
    data to evaluate any candidate meaningfully.
    """
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score

    n_samples = len(embeddings_array)

    # Silhouette Score requires 2 <= n_clusters < n_samples, and KMeans
    # itself requires n_clusters <= n_samples. Only keep candidates that
    # are strictly valid for the current dataset size.
    valid_ks = [k for k in CANDIDATE_K_VALUES if 2 <= k < n_samples]

    if not valid_ks:
        # Too few papers to safely evaluate any candidate K.
        # Fall back to the largest sensible value: 2 clusters if we have
        # at least 2 samples, otherwise a single cluster for everything.
        return min(2, n_samples) if n_samples >= 2 else 1

    best_k = valid_ks[0]
    best_score = -1.0

    for k in valid_ks:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(embeddings_array)
        score = silhouette_score(embeddings_array, labels)

        if score > best_score:
            best_score = score
            best_k = k

    return best_k


def run_kmeans(embeddings: list[list[float]]) -> list[int]:
    """
    Cluster embeddings using K-Means. The number of clusters (K) is not
    hardcoded — several candidate K values are evaluated using the
    Silhouette Score, and the best-scoring K is used for the final fit.
    Returns cluster labels in the same order as the input embeddings.

    Unlike HDBSCAN, K-Means has no "noise" concept — every paper is
    assigned to a cluster (labels are 0..K-1, never -1).
    """
    if not embeddings:
        return []

    from sklearn.cluster import KMeans

    embeddings_array = np.array(embeddings)

    if len(embeddings_array) < 2:
        # A single paper can't meaningfully form more than one cluster.
        return [0 for _ in embeddings]

    best_k = _select_best_k(embeddings_array)

    kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(embeddings_array)

    return [int(label) for label in labels]


def get_clustered_papers(db: Session) -> list[dict]:
    """
    Retrieve all paper embeddings from ChromaDB, run K-Means, and combine
    the resulting cluster assignments with full paper metadata from
    PostgreSQL (looked up by arxiv_id).
    """
    ids, embeddings = get_all_embeddings()
    if not ids:
        return []

    labels = run_kmeans(embeddings)

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


def get_clustered_papers_with_coordinates(db: Session) -> list[dict]:
    """
    Same as get_clustered_papers(), but also runs UMAP (unchanged) on the
    same embeddings to produce 2D (x, y) coordinates for visualization.
    cluster_id, x, and y all come from the same embedding set, so they
    stay consistent with each other.
    """
    ids, embeddings = get_all_embeddings()
    if not ids:
        return []

    labels = run_kmeans(embeddings)
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
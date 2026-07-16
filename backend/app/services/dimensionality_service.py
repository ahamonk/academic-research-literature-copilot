import numpy as np


def reduce_to_2d(embeddings: list[list[float]]) -> list[tuple[float, float]]:
    """
    Reduce high-dimensional embeddings to 2D (x, y) coordinates using UMAP,
    for later use in a cluster map visualization. Returns coordinates in
    the same order as the input embeddings.

    umap is imported here, not at module level, for the same reason as
    hdbscan in clustering_service.py — it has a heavy one-time import cost
    (numba JIT compilation) that should only be paid when this function is
    actually called, not on every app startup.
    """
    if len(embeddings) < 2:
        # Not enough points for UMAP to compute meaningful neighbors
        return [(0.0, 0.0) for _ in embeddings]

    import umap

    embeddings_array = np.array(embeddings)

    # UMAP requires n_neighbors < number of samples; keep it small and safe
    # for the currently small dataset while still allowing up to 15 as the
    # dataset grows.
    n_neighbors = max(2, min(15, len(embeddings) - 1))

    reducer = umap.UMAP(n_neighbors=n_neighbors, n_components=2, random_state=42)
    coordinates = reducer.fit_transform(embeddings_array)

    return [(float(x), float(y)) for x, y in coordinates]
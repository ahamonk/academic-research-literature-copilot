from sqlalchemy.orm import Session

from app.models.paper import Paper
from app.services.embedding_service import generate_embedding
from app.services.chroma_service import query_similar_papers


def semantic_search(db: Session, query: str, top_k: int) -> list[dict]:
    """
    Embed the query, find similar papers via ChromaDB, then fetch the
    complete, authoritative paper records from PostgreSQL.
    """
    query_embedding = generate_embedding(query)
    chroma_results = query_similar_papers(query_embedding, top_k)

    ids = chroma_results["ids"][0]
    distances = chroma_results["distances"][0]

    if not ids:
        return []

    papers = db.query(Paper).filter(Paper.arxiv_id.in_(ids)).all()
    papers_by_id = {paper.arxiv_id: paper for paper in papers}

    results = []
    for arxiv_id, distance in zip(ids, distances):
        paper = papers_by_id.get(arxiv_id)
        if paper is None:
            # Exists in Chroma but not Postgres (shouldn't normally happen
            # since both are written together during ingestion) — skip it
            # rather than returning incomplete data.
            continue

        similarity_score = round(1 / (1 + distance), 4)

        results.append(
            {
                "arxiv_id": paper.arxiv_id,
                "title": paper.title,
                "authors": paper.authors,
                "abstract": paper.abstract,
                "published_date": paper.published_date,
                "primary_category": paper.primary_category,
                "arxiv_url": paper.arxiv_url,
                "similarity_score": similarity_score,
            }
        )

    return results
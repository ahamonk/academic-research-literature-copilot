from sqlalchemy.orm import Session

from app.models.paper import Paper
from app.services.arxiv_service import fetch_papers_from_arxiv
from app.services.embedding_service import generate_embeddings
from app.services.chroma_service import add_papers_to_chroma


def save_new_papers(db: Session, papers: list[dict]) -> list[Paper]:
    """
    Given a list of parsed paper dicts (from arxiv_service), insert only the
    ones not already in the database (matched by arxiv_id). Returns the list
    of newly created Paper rows.
    """
    new_papers = []

    for paper_data in papers:
        existing = (
            db.query(Paper)
            .filter(Paper.arxiv_id == paper_data["arxiv_id"])
            .first()
        )
        if existing:
            continue

        paper = Paper(**paper_data)
        db.add(paper)
        new_papers.append(paper)

    db.commit()

    for paper in new_papers:
        db.refresh(paper)

    return new_papers


def _embed_and_store_papers(saved_papers: list[Paper]) -> None:
    """
    Generate embeddings for newly saved papers' abstracts and store them
    in ChromaDB, along with metadata needed for future semantic search.
    """
    if not saved_papers:
        return

    abstracts = [p.abstract for p in saved_papers]
    embeddings = generate_embeddings(abstracts)

    paper_dicts = [
        {
            "arxiv_id": p.arxiv_id,
            "abstract": p.abstract,
            "title": p.title,
            "authors": p.authors,
            "primary_category": p.primary_category,
            "published_date": p.published_date,
            "arxiv_url": p.arxiv_url,
        }
        for p in saved_papers
    ]

    add_papers_to_chroma(paper_dicts, embeddings)


def ingest_papers(db: Session, category: str, max_results: int) -> tuple[list[dict], list[Paper]]:
    """
    Full ingestion pipeline: fetch from arXiv, save new papers to Postgres,
    then embed and store the new papers in ChromaDB.
    Returns (fetched_papers, saved_papers).
    """
    fetched_papers = fetch_papers_from_arxiv(category=category, max_results=max_results)
    saved_papers = save_new_papers(db, fetched_papers)
    _embed_and_store_papers(saved_papers)

    return fetched_papers, saved_papers
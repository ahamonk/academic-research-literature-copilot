from sqlalchemy.orm import Session

from app.models.topic import Topic
from app.models.user_topic import UserTopic
from app.services.embedding_service import generate_embedding
from app.services.chroma_service import query_similar_papers
from app.services.paper_service import get_papers_by_arxiv_ids


def _get_user_topics(db: Session, user_id: int) -> list[Topic]:
    return (
        db.query(Topic)
        .join(UserTopic, UserTopic.topic_id == Topic.id)
        .filter(UserTopic.user_id == user_id)
        .all()
    )


def fetch_relevant_papers(db: Session, user_id: int, limit: int = 5) -> list[dict]:
    """
    Fetcher Agent (semantic version).

    Does NOT implement a second vector search pipeline. Instead:
      1. Reads the user's selected topics (arXiv category codes + names).
      2. Builds a single query embedding representing their overall
         research interests, using the SAME embedding_service.generate_embedding()
         function used everywhere else in this project.
      3. Calls the SAME chroma_service.query_similar_papers() function that
         powers /search, restricted via a metadata `where` filter to only
         the user's selected categories.
      4. Hydrates the ranked arxiv_id results with full PostgreSQL records
         (Postgres remains the source of truth for paper data).

    limit defaults to 5 (reduced from an earlier default of 15) to keep
    the downstream Summarizer/Critic/Trend Analyst pipeline's total
    number of sequential Groq calls manageable for interactive use and
    for n8n's HTTP request timeout.
    """
    user_topics = _get_user_topics(db, user_id)
    if not user_topics:
        return []

    category_codes = [t.arxiv_category_code for t in user_topics]
    topic_names = [t.name for t in user_topics]

    interest_query = ", ".join(topic_names)
    query_embedding = generate_embedding(interest_query)

    chroma_results = query_similar_papers(
        query_embedding,
        top_k=limit,
        where={"primary_category": {"$in": category_codes}},
    )

    ids = chroma_results["ids"][0]
    if not ids:
        return []

    papers_by_id = get_papers_by_arxiv_ids(db, ids)

    results = []
    for arxiv_id in ids:
        paper = papers_by_id.get(arxiv_id)
        if paper is None:
            continue
        results.append(
            {
                "arxiv_id": paper.arxiv_id,
                "title": paper.title,
                "authors": paper.authors,
                "abstract": paper.abstract,
                "published_date": paper.published_date,
                "primary_category": paper.primary_category,
                "arxiv_url": paper.arxiv_url,
            }
        )
    return results
from sqlalchemy.orm import Session

from app.graph.review_graph import get_review_graph


def generate_weekly_review(db: Session, user_id: int) -> dict:
    """
    Runs the full Fetcher -> Summarizer -> Critic -> Trend Analyst
    pipeline via the LangGraph graph and returns the generated literature
    review, the per-paper (Critic-reviewed, citation-numbered) summaries,
    and the matching references list.
    """
    graph = get_review_graph()

    initial_state = {
        "db": db,
        "user_id": user_id,
        "papers": [],
        "summarized_papers": [],
        "reviewed_papers": [],
        "literature_review": "",
        "references": [],
    }

    result = graph.invoke(initial_state)

    return {
        "literature_review": result["literature_review"],
        "papers": result["reviewed_papers"],
        "references": result["references"],
    }
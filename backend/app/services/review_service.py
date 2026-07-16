from sqlalchemy.orm import Session

from app.graph.review_graph import get_review_graph


def generate_weekly_review(db: Session, user_id: int) -> dict:
    """
    Runs the Fetcher -> Summarizer pipeline via the LangGraph graph and
    returns a list of summarized papers. No combined literature review is
    produced here — that will be the Trend Analyzer's responsibility once
    it's added to the graph.
    """
    graph = get_review_graph()

    initial_state = {
        "db": db,
        "user_id": user_id,
        "papers": [],
        "summarized_papers": [],
    }

    result = graph.invoke(initial_state)

    return {"papers": result["summarized_papers"]}
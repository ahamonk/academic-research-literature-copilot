from app.graph.state import ReviewState
from app.services.fetcher_service import fetch_relevant_papers
from app.services.summarizer_service import summarize_paper


def fetcher_node(state: ReviewState) -> dict:
    """
    LangGraph node wrapping the existing Fetcher Agent (fetcher_service.py).
    No business logic lives here — this is purely an adapter between the
    graph's state and the existing service function.
    """
    papers = fetch_relevant_papers(state["db"], state["user_id"])
    return {"papers": papers}


def summarizer_node(state: ReviewState) -> dict:
    """
    LangGraph node wrapping the existing Summarizer Agent
    (summarizer_service.py), applied once per fetched paper.
    """
    summarized_papers = []
    for paper in state["papers"]:
        summary = summarize_paper(paper)
        summarized_papers.append({**paper, "summary": summary})
    return {"summarized_papers": summarized_papers}
from app.graph.state import ReviewState
from app.services.fetcher_service import fetch_relevant_papers
from app.services.summarizer_service import summarize_paper
from app.services.critic_service import review_summary
from app.services.trend_analyzer_service import (
    assign_citations,
    generate_literature_review,
    build_references,
)


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


def critic_node(state: ReviewState) -> dict:
    """
    LangGraph node wrapping the Critic Agent (critic_service.py), applied
    once per summarized paper. Compares each paper's own summary against
    its own abstract and replaces 'summary' with the reviewed version —
    no cross-paper comparison happens here.
    """
    reviewed_papers = []
    for paper in state["summarized_papers"]:
        reviewed_summary = review_summary(paper)
        reviewed_papers.append({**paper, "summary": reviewed_summary})
    return {"reviewed_papers": reviewed_papers}


def trend_analyst_node(state: ReviewState) -> dict:
    """
    LangGraph node wrapping the Trend Analyst Agent
    (trend_analyzer_service.py). Unlike the earlier nodes, this one reads
    ALL reviewed papers together: citation numbers are assigned first
    (business logic, delegated to the service), then a single literature
    review is generated across every paper, and a matching references
    list is built.
    """
    cited_papers = assign_citations(state["reviewed_papers"])
    literature_review = generate_literature_review(cited_papers)
    references = build_references(cited_papers)

    return {
        "reviewed_papers": cited_papers,
        "literature_review": literature_review,
        "references": references,
    }
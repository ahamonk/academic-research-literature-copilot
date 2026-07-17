from langgraph.graph import StateGraph, START, END

from app.graph.state import ReviewState
from app.graph.nodes import (
    fetcher_node,
    summarizer_node,
    critic_node,
    trend_analyst_node,
)

_review_graph = None


def _build_review_graph():
    """
    Linear pipeline: START -> Fetcher -> Summarizer -> Critic
                            -> Trend Analyst -> END.

    This completes the architecture described in the original project
    sheet. Business logic for every node continues to live in its own
    service file (fetcher_service.py, summarizer_service.py,
    critic_service.py, trend_analyzer_service.py) — this file only wires
    them together in sequence.
    """
    graph = StateGraph(ReviewState)
    graph.add_node("fetcher", fetcher_node)
    graph.add_node("summarizer", summarizer_node)
    graph.add_node("critic", critic_node)
    graph.add_node("trend_analyst", trend_analyst_node)

    graph.add_edge(START, "fetcher")
    graph.add_edge("fetcher", "summarizer")
    graph.add_edge("summarizer", "critic")
    graph.add_edge("critic", "trend_analyst")
    graph.add_edge("trend_analyst", END)

    return graph.compile()


def get_review_graph():
    """
    Lazily build and cache the compiled graph on first use — consistent
    with the lazy-loading pattern used throughout this project to keep
    app startup fast.
    """
    global _review_graph
    if _review_graph is None:
        _review_graph = _build_review_graph()
    return _review_graph
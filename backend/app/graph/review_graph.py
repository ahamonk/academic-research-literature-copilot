from langgraph.graph import StateGraph, START, END

from app.graph.state import ReviewState
from app.graph.nodes import fetcher_node, summarizer_node

_review_graph = None


def _build_review_graph():
    """
    Linear pipeline: START -> Fetcher -> Summarizer -> END.

    Kept intentionally linear and minimal. Critic and Trend Analyzer nodes
    can be added later by:
      1. Writing new node functions in nodes.py (critic_node, trend_analyst_node)
      2. Adding them here via graph.add_node(...)
      3. Rewiring edges: fetcher -> summarizer -> critic -> trend_analyst -> END

    fetcher_service.py and summarizer_service.py themselves will not need
    to change for this — only this file's graph wiring will.
    """
    graph = StateGraph(ReviewState)
    graph.add_node("fetcher", fetcher_node)
    graph.add_node("summarizer", summarizer_node)

    graph.add_edge(START, "fetcher")
    graph.add_edge("fetcher", "summarizer")
    graph.add_edge("summarizer", END)

    return graph.compile()


def get_review_graph():
    """
    Lazily build and cache the compiled graph on first use — consistent
    with the lazy-loading pattern already used for the embedding model,
    ChromaDB client, and clustering libraries elsewhere in this project,
    to keep app startup fast.
    """
    global _review_graph
    if _review_graph is None:
        _review_graph = _build_review_graph()
    return _review_graph
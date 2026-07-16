from typing import TypedDict

from sqlalchemy.orm import Session


class ReviewState(TypedDict):
    """
    Shared state passed between LangGraph nodes in the review pipeline.

    db and user_id are inputs set before the graph runs.
    papers is populated by the Fetcher node.
    summarized_papers is populated by the Summarizer node.

    Designed to be extended later with e.g. "critiqued_papers" or
    "trend_summary" as the Critic and Trend Analyzer nodes are added,
    without needing to change how earlier nodes populate their own keys.
    """

    db: Session
    user_id: int
    papers: list[dict]
    summarized_papers: list[dict]
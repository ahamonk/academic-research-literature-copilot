from typing import TypedDict

from sqlalchemy.orm import Session


class ReviewState(TypedDict):
    """
    Shared state passed between LangGraph nodes in the review pipeline.

    db and user_id are inputs set before the graph runs.
    papers is populated by the Fetcher node.
    summarized_papers is populated by the Summarizer node.
    reviewed_papers is populated by the Critic node, and then updated by
    the Trend Analyst node to include citation numbers.
    literature_review and references are populated by the Trend Analyst
    node.
    """

    db: Session
    user_id: int
    papers: list[dict]
    summarized_papers: list[dict]
    reviewed_papers: list[dict]
    literature_review: str
    references: list[dict]
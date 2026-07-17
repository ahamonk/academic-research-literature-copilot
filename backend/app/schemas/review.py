from datetime import date

from pydantic import BaseModel


class SummarizedPaper(BaseModel):
    title: str
    authors: str
    abstract: str
    summary: str
    primary_category: str
    published_date: date
    arxiv_url: str
    citation: int | None = None


class ReferenceItem(BaseModel):
    citation: int
    title: str
    arxiv_url: str


class ReviewResponse(BaseModel):
    literature_review: str
    papers: list[SummarizedPaper]
    references: list[ReferenceItem]
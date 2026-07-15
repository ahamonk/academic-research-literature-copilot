from datetime import date, datetime

from pydantic import BaseModel


class PaperIngestRequest(BaseModel):
    category: str
    max_results: int = 20


class PaperResponse(BaseModel):
    id: int
    arxiv_id: str
    title: str
    abstract: str
    authors: str
    published_date: date
    arxiv_url: str
    primary_category: str
    created_at: datetime

    class Config:
        from_attributes = True


class PaperIngestResponse(BaseModel):
    fetched_count: int
    saved_count: int
    papers: list[PaperResponse]
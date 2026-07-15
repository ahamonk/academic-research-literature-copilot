from datetime import date

from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    top_k: int = 10


class SearchResultItem(BaseModel):
    arxiv_id: str
    title: str
    authors: str
    abstract: str
    published_date: date
    primary_category: str
    arxiv_url: str
    similarity_score: float


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResultItem]
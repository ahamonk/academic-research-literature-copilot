from datetime import date

from pydantic import BaseModel


class ClusterPaperResponse(BaseModel):
    arxiv_id: str
    title: str
    authors: str
    abstract: str
    primary_category: str
    published_date: date
    arxiv_url: str
    cluster_id: int
    x: float
    y: float
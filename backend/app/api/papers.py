from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.paper import PaperIngestRequest, PaperIngestResponse
from app.services.paper_service import ingest_papers

router = APIRouter(prefix="/papers", tags=["Papers"])


@router.post("/ingest", response_model=PaperIngestResponse)
def ingest(
    request: PaperIngestRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    fetched_papers, saved_papers = ingest_papers(
        db, category=request.category, max_results=request.max_results
    )

    return PaperIngestResponse(
        fetched_count=len(fetched_papers),
        saved_count=len(saved_papers),
        papers=saved_papers,
    )
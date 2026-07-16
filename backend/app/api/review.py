from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.review import ReviewResponse
from app.services.review_service import generate_weekly_review

router = APIRouter(prefix="/review", tags=["Review"])


@router.post("/generate", response_model=ReviewResponse)
def generate_review(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        result = generate_weekly_review(db, current_user.id)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return ReviewResponse(**result)
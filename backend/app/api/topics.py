from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.topic import TopicResponse, TopicSelectRequest, MessageResponse
from app.services.topic_service import get_all_topics, get_user_topics, set_user_topics

router = APIRouter(prefix="/topics", tags=["Topics"])


@router.get("", response_model=list[TopicResponse])
def list_topics(db: Session = Depends(get_db)):
    return get_all_topics(db)


@router.post("/select", response_model=MessageResponse)
def select_topics(
    request: TopicSelectRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    set_user_topics(db, current_user.id, request.topic_ids)
    return MessageResponse(message="Research interests updated successfully.")


@router.get("/my", response_model=list[TopicResponse])
def my_topics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_topics(db, current_user.id)
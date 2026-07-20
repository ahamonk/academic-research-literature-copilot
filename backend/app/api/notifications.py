from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import verify_service_api_key
from app.schemas.slack import ScheduledUserItem, SendReviewResponse
from app.services.notification_service import get_scheduled_users, send_weekly_review_to_user

router = APIRouter(tags=["Notifications"], dependencies=[Depends(verify_service_api_key)])


@router.get("/scheduled-users", response_model=list[ScheduledUserItem])
def scheduled_users(db: Session = Depends(get_db)):
    return get_scheduled_users(db)


@router.post("/notifications/send-review/{user_id}", response_model=SendReviewResponse)
def send_review(user_id: int, db: Session = Depends(get_db)):
    result = send_weekly_review_to_user(db, user_id)
    return SendReviewResponse(**result)
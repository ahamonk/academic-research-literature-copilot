from sqlalchemy import Column, Integer, Text, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class WeeklyReview(Base):
    __tablename__ = "weekly_reviews"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    week_start_date = Column(Date, nullable=False)
    week_end_date = Column(Date, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    topic = relationship("Topic", back_populates="weekly_reviews")
    review_papers = relationship("ReviewPaper", back_populates="review", cascade="all, delete-orphan")
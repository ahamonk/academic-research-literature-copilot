from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    arxiv_category_code = Column(String, nullable=False)
    discipline = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user_topics = relationship("UserTopic", back_populates="topic", cascade="all, delete-orphan")
    weekly_reviews = relationship("WeeklyReview", back_populates="topic", cascade="all, delete-orphan")
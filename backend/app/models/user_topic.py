from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class UserTopic(Base):
    __tablename__ = "user_topics"
    __table_args__ = (UniqueConstraint("user_id", "topic_id", name="uq_user_topic"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="user_topics")
    topic = relationship("Topic", back_populates="user_topics")
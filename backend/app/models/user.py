from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    slack_connected = Column(Boolean, nullable=False, default=False)
    slack_enabled = Column(Boolean, nullable=False, default=False)
    slack_access_token = Column(String, nullable=True)  # encrypted at rest
    slack_workspace_id = Column(String, nullable=True)
    slack_workspace_name = Column(String, nullable=True)
    slack_user_id = Column(String, nullable=True)

    user_topics = relationship("UserTopic", back_populates="user", cascade="all, delete-orphan")
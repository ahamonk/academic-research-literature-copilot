from sqlalchemy import Column, Integer, String, Text, Date, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    arxiv_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    abstract = Column(Text, nullable=False)
    authors = Column(String, nullable=False)
    published_date = Column(Date, nullable=False)
    arxiv_url = Column(String, nullable=False)
    primary_category = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    review_papers = relationship("ReviewPaper", back_populates="paper", cascade="all, delete-orphan")
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class ReviewPaper(Base):
    __tablename__ = "review_papers"
    __table_args__ = (UniqueConstraint("review_id", "paper_id", name="uq_review_paper"),)

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("weekly_reviews.id"), nullable=False)
    paper_id = Column(Integer, ForeignKey("papers.id"), nullable=False)

    review = relationship("WeeklyReview", back_populates="review_papers")
    paper = relationship("Paper", back_populates="review_papers")
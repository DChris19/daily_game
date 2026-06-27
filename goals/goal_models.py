from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    scheduled_at = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, default=False)
    streak_count = Column(Integer, default=0)
    last_completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="goals")
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class Release(Base):
    __tablename__ = "releases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    risk_score = Column(Float, default=0)
    regulatory_flags = Column(Text, default="")
    cost_of_delay = Column(Float, default=0)
    ai_reasoning = Column(Text, default="")
    status = Column(String, default="pending")  # pending, approved, rejected, deployed, rolled_back
    ba_comment = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
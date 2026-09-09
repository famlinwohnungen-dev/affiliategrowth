"""SQLAlchemy database models for Phase 3: Keyword Demand Discovery."""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class KeywordDemand(Base):
    """Search-demand signal for a niche keyword from a demand data source."""

    __tablename__ = "keyword_demand"

    id = Column(Integer, primary_key=True)
    niche_id = Column(String(255), nullable=False)
    niche_name = Column(String(255), nullable=False)
    keyword = Column(String(255), nullable=False)
    source = Column(String(50), nullable=False)
    geo = Column(String(5), default="DE")

    # Google Trends: 0-100 relative interest score (not absolute search volume).
    avg_interest = Column(Float)
    latest_interest = Column(Float)
    trend_direction = Column(String(20))
    related_queries = Column(Text)

    fetched_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<KeywordDemand(keyword='{self.keyword}', source='{self.source}', avg_interest={self.avg_interest})>"

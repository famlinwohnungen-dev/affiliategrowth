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

    # Keyword Planner: absolute volume. No-spend accounts return bucketed
    # ranges ("1000 - 10000"), so min/max are stored rather than one figure.
    search_volume_min = Column(Integer)
    search_volume_max = Column(Integer)
    competition = Column(String(20))
    competition_index = Column(Integer)
    cpc_low = Column(Float)
    cpc_high = Column(Float)

    fetched_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<KeywordDemand(keyword='{self.keyword}', source='{self.source}', avg_interest={self.avg_interest})>"


class NicheScore(Base):
    """Provisional Opportunity Score per niche.

    Provisional because two of the backlog's six components can't be computed
    yet: RevenuePotential needs commission rates Awin withholds for unjoined
    programmes, and SEOOpportunity needs Phase 4 SERP analysis. The remaining
    three are renormalised to 100, so a niche can score well here and still be
    unrealistic to rank for.
    """

    __tablename__ = "niche_scores"

    id = Column(Integer, primary_key=True)
    niche_id = Column(String(255), nullable=False, unique=True)
    niche_name = Column(String(255), nullable=False)
    parent_category = Column(String(255))

    search_demand = Column(Float)
    commercial_intent = Column(Float)
    affiliate_quality = Column(Float)
    opportunity_score = Column(Float)
    recommendation = Column(String(20))

    # Alternative ranking that treats competition as a cost rather than a
    # signal of value - "where can a new site win" vs "where is the money".
    winnability_score = Column(Float)
    winnability_recommendation = Column(String(20))

    # Kept for traceability of how each score was reached.
    search_volume = Column(Integer)
    trend_direction = Column(String(20))
    cpc_high = Column(Float)
    competition_index = Column(Integer)
    program_count = Column(Integer)

    scored_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<NicheScore(niche='{self.niche_name}', score={self.opportunity_score}, rec='{self.recommendation}')>"

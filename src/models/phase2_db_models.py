"""SQLAlchemy database models for Phase 2: Affiliate Program Discovery."""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Enum, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class CommissionType(str, enum.Enum):
    """Affiliate commission types."""
    CPS_PERCENT = "CPS_PERCENT"
    CPS_FIXED = "CPS_FIXED"
    CPL = "CPL"
    CPA_FIXED = "CPA_FIXED"
    CPC = "CPC"
    RECURRING = "RECURRING"
    UNKNOWN = "UNKNOWN"


class AffiliateProgram(Base):
    """Affiliate program from Awin/ADCELL networks."""

    __tablename__ = "affiliate_programs"

    id = Column(Integer, primary_key=True)
    source = Column(String(50), nullable=False)
    program_id = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    sector = Column(String(255))
    niche_category = Column(String(100))
    country = Column(String(2), default="DE")
    language = Column(String(5), default="de")
    website = Column(String(255))
    support_url = Column(String(255))
    commission_type = Column(Enum(CommissionType), default=CommissionType.UNKNOWN)
    commission_value = Column(Float)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    fetched_at = Column(DateTime)
    commissions = relationship("CommissionStructure", back_populates="program")

    def __repr__(self):
        return f"<AffiliateProgram(id={self.id}, name='{self.name}', source='{self.source}')>"


class CommissionStructure(Base):
    """Detailed commission structure for a program."""

    __tablename__ = "commission_structures"

    id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey("affiliate_programs.id"), nullable=False)
    tier_name = Column(String(100))
    commission_type = Column(Enum(CommissionType), nullable=False)
    commission_value = Column(Float, nullable=False)
    min_sales_volume = Column(Integer)
    min_clicks = Column(Integer)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    program = relationship("AffiliateProgram", back_populates="commissions")

    def __repr__(self):
        return f"<CommissionStructure(program_id={self.program_id}, type={self.commission_type})>"


class NicheProgramMapping(Base):
    """Maps niches from Phase 1 to affiliate programs."""

    __tablename__ = "niche_program_mappings"

    id = Column(Integer, primary_key=True)
    niche_id = Column(String(255), nullable=False)
    niche_name = Column(String(255), nullable=False)
    program_id = Column(Integer, ForeignKey("affiliate_programs.id"), nullable=False)
    program_name = Column(String(255), nullable=False)
    relevance_score = Column(Integer, default=0)
    is_verified = Column(Integer, default=0)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<NicheProgramMapping(niche='{self.niche_name}', program='{self.program_name}')>"

"""Pydantic models for niche data."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class NicheBase(BaseModel):
    """Base niche model."""

    name: str = Field(..., description="Niche name (e.g., 'Photovoltaik')")
    parent_category: str = Field(..., description="Parent category (e.g., 'Home & Energy')")
    description: Optional[str] = Field(None, description="Brief niche description")
    language: str = Field(default="de", description="Language code")
    country: str = Field(default="DE", description="Country code")


class NicheCreate(NicheBase):
    """Niche data for creation."""

    seed_keywords: list[str] = Field(
        default_factory=list, description="Seed keywords for initial research"
    )
    candidate_source: str = Field(
        default="affiliate_categories", description="Where this niche came from"
    )
    initial_affiliate_count: Optional[int] = Field(
        None, description="Initial estimate of available affiliate programs"
    )
    initial_search_signal: Optional[int] = Field(
        None, description="Initial Google search volume estimate"
    )


class Niche(NicheCreate):
    """Complete niche record."""

    niche_id: str = Field(..., description="Unique ID (slug)")
    status: str = Field(default="candidate", description="Status: candidate, active, archived")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

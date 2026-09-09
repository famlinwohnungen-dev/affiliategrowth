"""Tests for niche discovery."""

import pytest
from pathlib import Path

from src.pipelines.niche_discovery import (
    slugify,
    generate_niches_from_seeds,
)


def test_slugify():
    """Test slug generation."""
    assert slugify("Photovoltaik") == "photovoltaik"
    assert slugify("Home & Energy") == "home-energy"
    assert slugify("Wärmepumpe") == "warmepumpe"
    assert slugify("VPN Anbieter") == "vpn-anbieter"


def test_niche_generation():
    """Test niche generation from sample data."""
    categories = {
        "categories": {
            "test_category": {
                "name": "Test Category",
                "description": "A test category",
                "niches": ["Test Niche 1", "Test Niche 2"],
            }
        }
    }

    niches = generate_niches_from_seeds(categories)

    assert len(niches) == 2
    assert niches[0].name == "Test Niche 1"
    assert niches[0].parent_category == "Test Category"
    assert niches[0].language == "de"
    assert niches[0].country == "DE"


def test_niche_properties():
    """Test that generated niches have required properties."""
    categories = {
        "categories": {
            "energy": {
                "name": "Energy",
                "description": "Energy solutions",
                "niches": ["Solar"],
            }
        }
    }

    niches = generate_niches_from_seeds(categories)
    niche = niches[0]

    assert niche.niche_id is not None
    assert niche.name is not None
    assert niche.parent_category is not None
    assert niche.status == "candidate"
    assert niche.seed_keywords

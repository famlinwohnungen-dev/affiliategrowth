# Affiliate Intelligence MVP

**Germany Affiliate Niche Discovery System**

A data-driven research pipeline to validate whether German affiliate niches can generate repeatable revenue before investing in full automation.

## Core Question

> **Which German affiliate niches have enough search demand, commercial intent, achievable SERPs, and affiliate economics to justify publishing content?**

## MVP Goals

✅ Discover 50–100 candidate niches  
✅ Identify relevant affiliate programs (Awin, ADCELL)  
✅ Collect German search demand (Google Ads API)  
✅ Identify commercially relevant keywords  
✅ Analyze SERP competitors  
✅ Normalize affiliate commission models  
✅ Estimate revenue under multiple scenarios  
✅ Calculate Opportunity Score  
✅ Produce ranked recommendations: `BUILD`, `RESEARCH`, `BACKLOG`, `IGNORE`  

## Validation Path

```
50–100 candidates → Affiliate programs → Keywords → SERP analysis → Revenue modeling → Top 3 niches → Real content → Google traffic → Affiliate clicks → Revenue
```

## Quick Start

### Setup

```bash
# Clone and enter project
cd affiliate-intelligence

# Using uv (recommended)
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# OR using standard pip
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Initialize database
python -m src.db.init

# Verify setup
pytest tests/
```

### Environment

Create `.env`:

```
DATABASE_URL=sqlite:///./data/affiliate.db
AWIN_PUBLISHER_ID=
AWIN_ACCESS_TOKEN=
GOOGLE_ADS_CUSTOMER_ID=
GOOGLE_ADS_DEVELOPER_TOKEN=
GOOGLE_ADS_CLIENT_ID=
GOOGLE_ADS_CLIENT_SECRET=
GOOGLE_ADS_REFRESH_TOKEN=
```

(APIs optional for Phase 1)

## Project Structure

```
affiliate-intelligence/
├── pyproject.toml          # Dependencies
├── README.md               # This file
├── .env.example            # Template
├── .gitignore
│
├── config/
│   ├── niches.yaml         # Initial niche seeds
│   ├── scoring.yaml        # Scoring weights
│   └── countries.yaml      # Geo targets
│
├── src/
│   ├── config/             # Configuration loading
│   ├── db/                 # SQLAlchemy models, migrations
│   ├── models/             # Pydantic schemas
│   ├── sources/            # API collectors (awin.py, google_ads.py, etc)
│   ├── pipelines/          # ETL stages
│   │   ├── niche_discovery.py
│   │   ├── keyword_discovery.py
│   │   ├── serp_analysis.py
│   │   └── scoring.py
│   ├── analytics/          # Revenue calculations
│   └── reports/            # Export/visualization
│
├── sql/                    # SQL migrations
├── tests/                  # Pytest
├── notebooks/              # Jupyter exploration
└── data/                   # Local SQLite, cache
```

## Phases

### Phase 0 — Project Setup ✅
- [x] Repository structure
- [x] Dependencies
- [x] Git configuration

### Phase 1 — Niche Generation (Active)
- Generate 100 candidate niches from DACH categories
- Normalize and deduplicate
- Store in SQLite

### Phase 2 — Affiliate Programs
- Awin Publisher API integration (free tier)
- ADCELL account setup
- Program collection and normalization

### Phase 3 — Google Keyword Data
- Germany + German language targeting
- Keyword idea generation
- Search volume and competition data

### Phase 4 — SERP Analysis
- DataForSEO (free tier) or alternative
- Top 10 organic results per keyword
- Competitor analysis

### Phase 5 — Revenue Modeling
- Scenario-based estimation (conservative/base/optimistic)
- Traffic assumptions at 10k/50k/100k visitors
- Commission normalization

### Phase 6 — Opportunity Scoring
- Weighted scoring formula
- Recommendation engine (BUILD/RESEARCH/BACKLOG/IGNORE)
- Ranked output

### Phase 7 — Real-World Validation
- Select top 3 niches
- Publish 30–45 high-value pages
- Track Google impressions, rankings, affiliate clicks, revenue

## Key Principles

**No assumptions.** Every metric carries source, retrieval timestamp, and confidence level.

**Predict → Experiment → Validate → Scale.** Do not automate the next layer until the previous one shows economic value.

**Simplicity first.** Python + SQLite. No Kubernetes, microservices, or agents yet.

**Hard budget, always.** Set API cost limits upfront. No surprises.

## Current Status

**Phase 1: Niche Generation**

Generating initial 100+ niches from DACH affiliate network categories.

## Next Steps

1. Generate niche seed list
2. Set up SQLite schema
3. Store first candidates in database
4. Move to Phase 2 (Affiliate programs)

## References

- Full spec: `IDEAS.md`
- Implementation backlog: `affiliate_niche_intelligence_mvp_backlog.md`
- Behavioral rules: `CLAUDE.md`, `AGENTS.md`

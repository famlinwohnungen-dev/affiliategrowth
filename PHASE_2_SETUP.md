# Phase 2: Affiliate Program Discovery — Setup Guide

## Status
✅ **Awin**: Verified and ready  
⏳ **ADCELL**: Pending approval (tomorrow)

## What's New in Phase 2

Phase 2 adds database persistence and affiliate program collection:

- **Database**: SQLite with SQLAlchemy ORM
- **Awin Collector**: Fetches available programmes from Awin API
- **Programme Models**: Store programmes, commissions, niche mappings
- **Extensible**: Ready for ADCELL when it comes

## Files Generated

```
phase2_db_models.py         # SQLAlchemy models (AffiliateProgram, CommissionStructure, NicheProgramMapping)
awin_collector.py           # Awin API client
phase2_pipeline.py          # Main Phase 2 pipeline (fetch, store, report)
```

## Setup Instructions

### 1. Add to `.env` file (in ~/Dev/affiliategrowth/)

```env
AWIN_TOKEN=<dein Awin API-Token>
AWIN_PUBLISHER_ID=<deine Publisher-ID>
```

> **Niemals echte Zugangsdaten in dieses Repository schreiben.** Es ist
> öffentlich. Tokens gehören ausschließlich in `.env`, das über `.gitignore`
> ausgeschlossen ist. Ein hier einmal committeter Token ist dauerhaft
> kompromittiert und muss bei Awin neu erzeugt werden.

Ein Pre-Commit-Hook prüft darauf. Einmalig pro Klon aktivieren:

```bash
git config core.hooksPath .githooks
```

### 2. Install additional dependencies

In your activated venv:

```bash
pip install sqlalchemy python-dotenv requests
```

### 3. Copy files to your project

Move the generated files to your project:

```bash
# Copy models and collectors
cp phase2_db_models.py ~/Dev/affiliategrowth/src/models/
cp awin_collector.py ~/Dev/affiliategrowth/src/sources/
cp phase2_pipeline.py ~/Dev/affiliategrowth/

# Or manually copy them into the right directories
```

### 4. Run Phase 2 pipeline

```bash
cd ~/Dev/affiliategrowth
source venv/bin/activate
python phase2_pipeline.py
```

This will:
1. Create the database (`data/affiliate_programs.db`)
2. Fetch available programmes from Awin
3. Store them in the database
4. Generate a Phase 2 report (`data/PHASE_2_REPORT.md`)

## What Happens

When you run `python phase2_pipeline.py`:

```
PHASE 2: AFFILIATE PROGRAM DISCOVERY
============================================================

Fetching available programmes from Awin...
  Fetched 500 programmes (offset: 0)
  Fetched 500 programmes (offset: 500)
  ... (continues until all fetched)
  
✓ Total programmes fetched: X

Storing X programmes in database...
  Processed 100/X programmes
  ...
✓ Stored X programmes

✓ Database initialized: data/affiliate_programs.db

PHASE 2 STATUS REPORT
============================================================
Total Programmes: X
  - Awin: X
  - ADCELL: 0

Active Programmes: X

Next Steps:
1. Wait for ADCELL approval
2. Implement ADCELL collector
3. Map programmes to niches
4. Normalize commissions
5. Export to CSV/JSON
============================================================
```

## Database Schema

### affiliate_programs table
- `id` — Primary key
- `source` — "awin" or "adcell"
- `program_id` — External ID
- `name` — Programme name
- `description` — Full description
- `website` — Programme website
- `country` — Country code (default: DE)
- `commission_type` — Type of commission (CPS_PERCENT, CPL, etc.)
- `commission_value` — Commission amount/percentage
- `is_active` — Active status
- `fetched_at` — When data was fetched
- `created_at` / `updated_at` — Timestamps

### commission_structures table
- Supports multiple commission tiers per programme
- Links to `affiliate_programs.id`

### niche_program_mappings table
- Maps Phase 1 niches to Phase 2 programmes
- Relevance scoring (0-100)
- Manual verification flag

## Next: ADCELL Integration (Tomorrow)

Once ADCELL approves and provides credentials:

1. Get ADCELL Publisher ID and API key
2. Add to `.env`:
   ```env
   ADCELL_TOKEN=YOUR_TOKEN
   ADCELL_PUBLISHER_ID=YOUR_ID
   ```
3. Implement ADCELL collector (similar to Awin)
4. Update Phase 2 pipeline to fetch both sources
5. Run pipeline again to combine all programmes

## Testing

Test individual components:

```bash
# Test Awin collector
python -c "from awin_collector import AwinCollector; collector = AwinCollector('YOUR_TOKEN', 3083037); print(collector.get_available_programmes(limit=10))"

# Query database
python -c "from sqlalchemy import create_engine; from src.models.affiliate_program import AffiliateProgram; engine = create_engine('sqlite:///data/affiliate_programs.db'); print(engine.execute('SELECT COUNT(*) FROM affiliate_programs').fetchone())"
```

## Troubleshooting

**"ModuleNotFoundError: No module named 'sqlalchemy'"**
```bash
pip install sqlalchemy
```

**"AWIN_TOKEN or AWIN_PUBLISHER_ID not set"**
Make sure `.env` file exists in project root with credentials.

**"404 NOT_FOUND from Awin API"**
Verify AWIN_PUBLISHER_ID is correct (numeric only, no quotes).

**Empty array returned from Awin**
This is normal if you just joined. The pipeline will still work and store data when programmes are available.

---

Ready to run Phase 2? Follow the setup instructions above, then execute `python phase2_pipeline.py`.

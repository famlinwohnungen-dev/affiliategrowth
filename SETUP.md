# Setup Guide

## Prerequisites

- Python 3.12+
- Git
- uv (recommended) or pip

## 1. Clone the Repository

```bash
# You'll do this after creating the GitHub repo
git clone https://github.com/YOUR_USERNAME/affiliate-intelligence.git
cd affiliate-intelligence
```

## 2. Create Virtual Environment

### Using uv (recommended)

```bash
# Install uv if you haven't
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e ".[dev]"
```

### Using standard pip

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

## 3. Copy Environment Variables

```bash
cp .env.example .env
```

(Leave API credentials empty for now — we'll add them in later phases)

## 4. Run Tests

```bash
pytest tests/ -v
```

Expected output: All tests should pass.

## 5. Generate Initial Niches

```bash
python main.py
```

This will:
- Read `config/niches.yaml` (162 DACH niches)
- Generate normalized niche records
- Export to `data/niches_export.csv` and `data/niches_export.json`
- Create `data/NICHE_GENERATION_REPORT.md`

Expected output: 162 niches generated

## 6. Review Output

```bash
# Read the report
cat data/NICHE_GENERATION_REPORT.md

# Preview CSV (if you have less on your system)
head -20 data/niches_export.csv

# Check JSON structure
head -50 data/niches_export.json
```

## Project Structure After Setup

```
affiliate-intelligence/
├── .env.example
├── .env                    # Local (git-ignored)
├── .git/                   # After git init
├── .gitignore
├── pyproject.toml
├── README.md
├── SETUP.md
├── main.py
│
├── config/
│   ├── niches.yaml         # 162 DACH niche seeds
│   └── ...
│
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── niche.py        # Pydantic models
│   ├── pipelines/
│   │   ├── __init__.py
│   │   ├── niche_discovery.py  # ← Phase 1
│   │   ├── keyword_discovery.py  # ← Phase 3
│   │   ├── serp_analysis.py      # ← Phase 4
│   │   └── scoring.py             # ← Phase 6
│   └── ...
│
├── tests/
│   ├── __init__.py
│   └── test_niche_discovery.py
│
└── data/
    ├── niches_export.csv       # Generated
    ├── niches_export.json      # Generated
    └── NICHE_GENERATION_REPORT.md  # Generated
```

## Next: Phase 2 — Affiliate Programs

Once you've verified the niche generation works:

1. Create Awin publisher account
2. Get API credentials
3. Add to `.env`
4. Implement `AwinCollector` in `src/sources/awin.py`
5. Run Phase 2 pipeline

See the full spec: `IDEAS.md` and `affiliate_niche_intelligence_mvp_backlog.md`

## Troubleshooting

### "ModuleNotFoundError: No module named 'src'"

Make sure you're running from the project root and the venv is activated.

### "YAML not found"

Check that `config/niches.yaml` exists and the path in `main.py` is correct.

### Tests fail

Check that pytest is installed:

```bash
pip install pytest
```

## Support

Refer to:
- `CLAUDE.md` — behavioral rules
- `AGENTS.md` — working style
- `IDEAS.md` — full specification

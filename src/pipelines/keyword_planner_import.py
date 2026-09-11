"""Import a Google Ads Keyword Planner CSV export into keyword_demand.

Use the plan's "Bisherige Messwerte" / "Historical metrics" export, which has
one row per keyword. The "Prognosen"/"Forecasts" export is campaign-level and
carries no per-keyword search volume.

Google Ads exports are UTF-16 with tab separators and a few preamble lines
before the header row, and locale decides whether numbers use "," or "." as
the decimal separator. Accounts without spend report volume as a bucketed
range ("1000 - 10000") rather than a single figure.
"""

import argparse
import csv
import io
import re
import sys
from datetime import datetime
from pathlib import Path

project_root = str(Path(__file__).resolve().parents[2])
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

from src.models.phase3_db_models import Base, KeywordDemand

SOURCE = "google_keyword_planner"

# Header labels differ by export locale.
KEYWORD_COLS = ["keyword", "keywords", "suchbegriff"]
VOLUME_COLS = ["avg. monthly searches", "avg monthly searches", "durchschn. suchanfragen pro monat"]
COMPETITION_COLS = ["competition", "wettbewerb"]
COMPETITION_INDEX_COLS = ["competition (indexed value)", "wettbewerb (indexierter wert)"]
CPC_LOW_COLS = ["top of page bid (low range)", "gebot für obere seitenposition (unterer bereich)"]
CPC_HIGH_COLS = ["top of page bid (high range)", "gebot für obere seitenposition (oberer bereich)"]


# Export locale decides the competition labels; downstream scoring shouldn't care.
COMPETITION_NORMALISED = {
    "hoch": "High",
    "mittel": "Medium",
    "niedrig": "Low",
    "high": "High",
    "medium": "Medium",
    "low": "Low",
}


def decode_export(path: str) -> str:
    raw = Path(path).read_bytes()
    for enc in ("utf-16", "utf-8-sig", "utf-8", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Could not decode {path}")


def find_header_row(lines: list) -> int:
    """Google prepends preamble lines; the header is the first row naming a keyword column."""
    for i, line in enumerate(lines):
        cells = [c.strip().strip('"').lower() for c in line.split("\t")]
        if any(c in KEYWORD_COLS for c in cells):
            return i
    raise ValueError(
        "No keyword column found. This looks like a Forecasts export - "
        "re-download from the plan's 'Bisherige Messwerte' / 'Historical metrics' view."
    )


def pick(row: dict, candidates: list):
    for key, value in row.items():
        if key and key.strip().strip('"').lower() in candidates:
            return value
    return None


def parse_number(value: str):
    """Parse a locale-formatted number. '1.234,56' -> 1234.56, '1,234.56' -> 1234.56"""
    if not value:
        return None
    v = str(value).strip().strip('"').replace(" ", "").replace(" ", "")
    if not v or v in {"-", "--"}:
        return None
    if "," in v and "." in v:
        # Whichever separator comes last is the decimal one.
        v = v.replace(".", "").replace(",", ".") if v.rfind(",") > v.rfind(".") else v.replace(",", "")
    elif "," in v:
        # Comma is decimal separator if it's followed by 1-2 digits, else thousands.
        v = v.replace(",", ".") if re.search(r",\d{1,2}$", v) else v.replace(",", "")
    else:
        v = v.replace(".", "") if re.search(r"\.\d{3}(\D|$)", v) else v
    try:
        return float(v)
    except ValueError:
        return None


def parse_volume_range(value: str):
    """'1000 - 10000' -> (1000, 10000); '12100' -> (12100, 12100)."""
    if not value:
        return None, None
    v = str(value).strip().strip('"')
    if not v or v in {"-", "--", "0"}:
        return None, None

    parts = re.split(r"\s*[-–—]\s*", v)
    if len(parts) == 2:
        lo, hi = parse_number(parts[0]), parse_number(parts[1])
        if lo is not None and hi is not None:
            return int(lo), int(hi)

    n = parse_number(v)
    return (int(n), int(n)) if n is not None else (None, None)


def ensure_columns(engine):
    """SQLite: add the Keyword Planner columns to an existing table."""
    Base.metadata.create_all(engine)
    existing = {c["name"] for c in inspect(engine).get_columns("keyword_demand")}
    additions = {
        "search_volume_min": "INTEGER",
        "search_volume_max": "INTEGER",
        "competition": "VARCHAR(20)",
        "competition_index": "INTEGER",
        "cpc_low": "FLOAT",
        "cpc_high": "FLOAT",
    }
    with engine.begin() as conn:
        for col, coltype in additions.items():
            if col not in existing:
                conn.execute(text(f"ALTER TABLE keyword_demand ADD COLUMN {col} {coltype}"))
                print(f"  + added column {col}")


def normalise_keyword(value: str) -> str:
    """Google strips punctuation from keywords ('Kfz-Versicherung' -> 'kfz versicherung'),
    so both sides are flattened to compare."""
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", value.lower(), flags=re.UNICODE)).strip()


def load_niche_lookup(session) -> dict:
    """Map normalised niche name -> (niche_id, niche_name) using the Trends rows."""
    rows = session.query(KeywordDemand.niche_id, KeywordDemand.niche_name).filter_by(
        source="google_trends"
    ).all()
    return {normalise_keyword(name): (nid, name) for nid, name in rows}


def import_export(csv_path: str, db_path: str = "data/affiliate_programs.db", geo: str = "DE") -> int:
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    ensure_columns(engine)
    session = sessionmaker(bind=engine)()

    text_data = decode_export(csv_path)
    lines = text_data.splitlines()
    header_idx = find_header_row(lines)
    reader = csv.DictReader(io.StringIO("\n".join(lines[header_idx:])), delimiter="\t")

    lookup = load_niche_lookup(session)
    imported = 0
    unmatched = []

    for row in reader:
        keyword = (pick(row, KEYWORD_COLS) or "").strip().strip('"')
        if not keyword:
            continue

        vol_min, vol_max = parse_volume_range(pick(row, VOLUME_COLS))
        comp_index = parse_number(pick(row, COMPETITION_INDEX_COLS))

        niche_id, niche_name = lookup.get(normalise_keyword(keyword), (None, None))
        if niche_id is None:
            unmatched.append(keyword)
            niche_id, niche_name = f"unmatched_{keyword.lower().replace(' ', '_')}", keyword

        existing = session.query(KeywordDemand).filter_by(niche_id=niche_id, source=SOURCE).first()
        target = existing or KeywordDemand(
            niche_id=niche_id, niche_name=niche_name, keyword=keyword, source=SOURCE, geo=geo
        )

        target.search_volume_min = vol_min
        target.search_volume_max = vol_max
        raw_comp = (pick(row, COMPETITION_COLS) or "").strip().strip('"')
        target.competition = COMPETITION_NORMALISED.get(raw_comp.lower(), raw_comp or None)
        target.competition_index = int(comp_index) if comp_index is not None else None
        target.cpc_low = parse_number(pick(row, CPC_LOW_COLS))
        target.cpc_high = parse_number(pick(row, CPC_HIGH_COLS))
        target.fetched_at = datetime.utcnow()

        if existing is None:
            session.add(target)
        imported += 1

    session.commit()
    session.close()

    if imported == 0:
        print(
            f"\n❌ No keyword rows found in {Path(csv_path).name}.\n"
            "   The 'Keyword' column exists but every row is empty, which is what a\n"
            "   Forecasts export looks like - it reports campaign totals, not keywords.\n"
            "   Re-download from the plan's 'Bisherige Messwerte' / 'Historical metrics'\n"
            "   view instead."
        )
        return 0

    print(f"\n✓ Imported {imported} keywords from {Path(csv_path).name}")
    if unmatched:
        print(f"⚠ {len(unmatched)} keyword(s) did not match a known niche: {unmatched[:10]}")
    return imported


def main():
    parser = argparse.ArgumentParser(description="Import a Keyword Planner CSV export")
    parser.add_argument("csv_path", help="Path to the Keyword Planner historical-metrics CSV")
    parser.add_argument("--db", default="data/affiliate_programs.db")
    args = parser.parse_args()

    return 0 if import_export(args.csv_path, db_path=args.db) > 0 else 1


if __name__ == "__main__":
    sys.exit(main())

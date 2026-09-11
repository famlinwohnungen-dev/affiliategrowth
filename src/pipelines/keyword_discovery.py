"""Phase 3: Keyword Demand Discovery via Google Trends.

Fetches relative search-interest for every Phase 1 niche keyword and stores
it for triage. This is free but rate-limited and gives only relative
interest (0-100), not absolute search volume - treat as a first-pass filter
before spending on a commercial keyword API for the shortlisted niches.
"""

import csv
import sys
from datetime import datetime
from pathlib import Path

project_root = str(Path(__file__).resolve().parents[2])
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.phase3_db_models import Base, KeywordDemand
from src.sources.google_trends_collector import GoogleTrendsCollector


def init_database(db_path: str = "data/affiliate_programs.db") -> object:
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session


def load_niches(csv_path: str) -> list:
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fetch_keyword_demand(
    session_factory,
    niches_csv: str = "data/niches_export.csv",
    geo: str = "DE",
    request_delay: float = 15.0,
    limit: int = None,
    only_missing: bool = False,
) -> int:
    niches = load_niches(niches_csv)

    if only_missing:
        session = session_factory()
        done = {
            row[0]
            for row in session.query(KeywordDemand.niche_id).filter_by(source="google_trends").all()
        }
        session.close()
        niches = [n for n in niches if n["niche_id"] not in done]

    if limit:
        niches = niches[:limit]

    if not niches:
        print("✓ Nothing to fetch - all niches already have demand data")
        return 0

    print("\n" + "=" * 60)
    print("PHASE 3: KEYWORD DEMAND DISCOVERY (Google Trends)")
    print("=" * 60)
    print(f"\nFetching demand for {len(niches)} niches (geo={geo})...")
    print(f"Rate-limit pacing: {request_delay}s between requests")
    print(f"Estimated time: ~{len(niches) * request_delay / 60:.0f} min\n")

    collector = GoogleTrendsCollector(geo=geo, request_delay=request_delay)
    session = session_factory()
    stored = 0

    try:
        for i, niche in enumerate(niches):
            keyword = niche["name"]
            print(f"[{i + 1}/{len(niches)}] {keyword}")

            result = collector.get_keyword_interest(keyword)
            if i < len(niches) - 1:
                import time
                time.sleep(request_delay)

            if not result:
                continue

            existing = session.query(KeywordDemand).filter_by(
                niche_id=niche["niche_id"], source="google_trends"
            ).first()

            if existing:
                existing.avg_interest = result["avg_interest"]
                existing.latest_interest = result["latest_interest"]
                existing.trend_direction = result["trend_direction"]
                existing.fetched_at = datetime.utcnow()
            else:
                session.add(KeywordDemand(
                    niche_id=niche["niche_id"],
                    niche_name=niche["name"],
                    keyword=keyword,
                    source="google_trends",
                    geo=geo,
                    avg_interest=result["avg_interest"],
                    latest_interest=result["latest_interest"],
                    trend_direction=result["trend_direction"],
                    fetched_at=datetime.utcnow(),
                ))

            stored += 1
            if stored % 10 == 0:
                session.commit()

        session.commit()
        print(f"\n✓ Stored demand data for {stored} niches")
        return stored

    except Exception as e:
        session.rollback()
        print(f"❌ Error storing keyword demand: {e}")
        return stored
    finally:
        session.close()


def generate_report(session_factory, output_path: str = "data/PHASE_3_KEYWORD_DEMAND_REPORT.md"):
    session = session_factory()
    try:
        rows = (
            session.query(KeywordDemand)
            .filter_by(source="google_trends")
            .order_by(KeywordDemand.avg_interest.desc())
            .all()
        )

        lines = [
            "# Phase 3: Keyword Demand Report (Google Trends)",
            "",
            f"Total niches with demand data: {len(rows)}",
            "",
            "_Note: `avg_interest`/`latest_interest` are Google Trends' relative 0-100",
            "scale, not absolute monthly search volume. Use for triage/ranking only._",
            "",
            "| Niche | Avg Interest | Latest | Trend |",
            "|---|---|---|---|",
        ]
        for row in rows:
            lines.append(
                f"| {row.niche_name} | {row.avg_interest:.0f} | {row.latest_interest:.0f} | {row.trend_direction} |"
            )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

        print(f"✓ Report saved: {output_path}")

    finally:
        session.close()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Fetch Google Trends keyword demand for niches")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of niches (for testing)")
    parser.add_argument("--delay", type=float, default=15.0, help="Seconds between Trends requests")
    parser.add_argument(
        "--only-missing",
        action="store_true",
        help="Only fetch niches with no stored demand data yet (retry after rate-limiting)",
    )
    args = parser.parse_args()

    Session = init_database()
    stored = fetch_keyword_demand(
        Session, limit=args.limit, request_delay=args.delay, only_missing=args.only_missing
    )

    if stored > 0:
        generate_report(Session)
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())

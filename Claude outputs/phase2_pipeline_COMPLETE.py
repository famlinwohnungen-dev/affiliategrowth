"""Phase 2: Affiliate Program Discovery Pipeline."""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = str(Path(__file__).parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.phase2_db_models import Base, AffiliateProgram, CommissionType
from src.sources.awin_collector import AwinCollector


def init_database(db_path: str = "data/affiliate_programs.db") -> object:
    """Initialize SQLite database for Phase 2."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    print(f"✓ Database initialized: {db_path}")
    return Session


def fetch_awin_programmes(session_factory) -> int:
    """Fetch and store Awin programmes."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("❌ python-dotenv not installed. Run: pip install python-dotenv")
        return 0

    load_dotenv()

    token = os.getenv("AWIN_TOKEN")
    publisher_id = int(os.getenv("AWIN_PUBLISHER_ID", 0))

    if not token or not publisher_id:
        print("❌ AWIN_TOKEN and AWIN_PUBLISHER_ID must be set in .env")
        return 0

    print("\n" + "=" * 60)
    print("PHASE 2: AFFILIATE PROGRAM DISCOVERY")
    print("=" * 60)
    print()

    # Fetch programmes
    collector = AwinCollector(token=token, publisher_id=publisher_id)
    programmes = collector.fetch_all_available(batch_size=100)

    if not programmes:
        print("❌ No programmes fetched from Awin")
        return 0

    # Store in database
    session = session_factory()
    stored_count = 0

    try:
        print(f"\nStoring {len(programmes)} programmes in database...")

        for raw_prog in programmes:
            # Check if already exists
            existing = session.query(AffiliateProgram).filter_by(
                source="awin",
                program_id=str(raw_prog.get("id", ""))
            ).first()

            if existing:
                existing.updated_at = datetime.utcnow()
                existing.fetched_at = datetime.utcnow()
            else:
                prog = AffiliateProgram(
                    source="awin",
                    program_id=str(raw_prog.get("id", "")),
                    name=raw_prog.get("name", ""),
                    description=raw_prog.get("description", ""),
                    website=raw_prog.get("websiteUrl", ""),
                    support_url=raw_prog.get("supportUrl", ""),
                    country=raw_prog.get("country", "DE"),
                    language=raw_prog.get("language", "de"),
                    is_active=1 if raw_prog.get("status") == "active" else 0,
                    commission_type=CommissionType.UNKNOWN,
                    fetched_at=datetime.utcnow(),
                )
                session.add(prog)

            stored_count += 1

            if stored_count % 100 == 0:
                print(f"  Processed {stored_count}/{len(programmes)} programmes")

        session.commit()
        print(f"\n✓ Stored {stored_count} programmes")
        return stored_count

    except Exception as e:
        session.rollback()
        print(f"❌ Error storing programmes: {e}")
        return 0
    finally:
        session.close()


def generate_phase2_report(session_factory):
    """Generate Phase 2 status report."""
    session = session_factory()

    try:
        total = session.query(AffiliateProgram).count()
        awin = session.query(AffiliateProgram).filter_by(source="awin").count()
        adcell = session.query(AffiliateProgram).filter_by(source="adcell").count()
        active = session.query(AffiliateProgram).filter_by(is_active=1).count()

        report = f"""
PHASE 2 STATUS REPORT
{'=' * 60}

Total Programmes: {total}
  - Awin: {awin}
  - ADCELL: {adcell}

Active Programmes: {active}

Database: data/affiliate_programs.db

Next Steps:
1. Wait for ADCELL approval
2. Implement ADCELL collector
3. Map programmes to Phase 1 niches
4. Normalize commission structures
5. Generate affiliate_programs export (CSV/JSON)

{'=' * 60}
"""
        print(report)

        os.makedirs("data", exist_ok=True)
        with open("data/PHASE_2_REPORT.md", "w") as f:
            f.write(report)

        print("✓ Report saved: data/PHASE_2_REPORT.md")

    finally:
        session.close()


def main():
    """Run Phase 2 pipeline."""
    print()

    Session = init_database()
    stored = fetch_awin_programmes(Session)

    if stored > 0:
        generate_phase2_report(Session)
        print()
        print("=" * 60)
        print("✅ PHASE 2 SETUP COMPLETE")
        print("=" * 60)
        return 0
    else:
        print()
        print("❌ Phase 2 failed: No programmes stored")
        return 1


if __name__ == "__main__":
    sys.exit(main())

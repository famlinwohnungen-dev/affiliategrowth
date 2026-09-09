"""Phase 2b: Map Phase 1 niches to Awin/ADCELL affiliate programmes.

Awin programmes carry an English `primarySector` (e.g. "Automotive",
"Health & Beauty"). Phase 1 niches carry a German name plus an English
`parent_category` (e.g. "Automotive", "Beauty & Personal Care"). We match
niche -> programme primarily by sector, and use keyword overlap in the
programme name/description as a secondary signal, since Awin has no
per-programme keyword field to match a niche's specific German term against.
"""

import csv
import os
import sys
from pathlib import Path

project_root = str(Path(__file__).resolve().parents[2])
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.phase2_db_models import AffiliateProgram, NicheProgramMapping

# Maps a Phase 1 niche parent_category to the Awin `primarySector` values
# that are relevant to it. One category can map to several sectors.
CATEGORY_TO_SECTORS = {
    "Home & Energy": ["Home & Garden", "Utilities", "Green (Eco friendly)", "B2B Utility Services"],
    "Finance & Insurance": ["Insurance", "Loans", "Mortgages", "Savings & Investments", "Personal Banking", "Credit Cards"],
    "Telecommunications": ["Mobile Contract", "Mobile Broadband", "Mobile Pay As You Go", "Internet Service Provider", "Network Operators", "B2B Telecommunications Services"],
    "Software & SaaS": ["Software Downloads", "Web Hosting", "Business Services (B2B)"],
    "Education & Learning": ["Education, Training & Recruitment"],
    "Travel & Hospitality": ["Hotels & Accommodation", "Airlines", "Travel Agencies", "Cruises/Ferries", "Car Rental", "Tourism & Attractions", "Local Holidays", "Airport Parking & Transfers", "Trains"],
    "Health & Wellness": ["Health & Beauty", "Pharmaceuticals"],
    "Home & Garden": ["Home & Garden", "Furniture & Soft Furnishings", "DIY", "White Goods"],
    "Consumer Electronics": ["Computers", "Electronic Superstore", "Electronic Accessories", "Gadgets", "Audio Visual"],
    "Automotive": ["Automotive", "Car Rental"],
    "Beauty & Personal Care": ["Health & Beauty"],
    "Sports & Outdoor": ["Sports Equipment", "Sportswear"],
    "Pets": ["Pets & Pet Care"],
    "Home Security": ["Home & Garden"],
    "Media & Streaming": ["Digital TV & Video-on-Demand", "Entertainment Downloads", "Music & DVD", "Books & Subscriptions"],
    "Dating & Social": ["Dating"],
    "Food & Drinks": ["FMCG", "Wine, Spirits & Tobacco"],
    "Gaming": ["Online Gaming", "PC & Video Games", "Gambling & Competitions"],
    "B2B & Professional Services": ["Business Services (B2B)", "Office Supplies", "Lead Gen"],
    "Transport & Logistics": ["Trains", "Car Rental", "Airport Parking & Transfers"],
    "Fashion & Clothing": ["Clothing", "Clothing Accessories", "Menswear", "Womenswear", "Childrenswear", "Shoes", "Jewellery", "Lingerie"],
    "Crafts & DIY": ["DIY", "Office Supplies"],
}

SECTOR_SCORE = 60
KEYWORD_SCORE = 8
MAX_KEYWORD_BONUS = 40


def load_niches(csv_path: str) -> list:
    niches = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            niches.append(row)
    return niches


def niche_keywords(niche: dict) -> list:
    """English-ish keyword tokens usable against program name/description."""
    tokens = niche["name"].lower().replace("-", " ").replace("/", " ").split()
    tokens += niche["parent_category"].lower().replace("&", " ").split()
    return [t for t in set(tokens) if len(t) > 2]


def score_program(niche: dict, keywords: list, program: AffiliateProgram, sectors: list) -> int:
    score = 0
    if program.sector in sectors:
        score += SECTOR_SCORE

    haystack = f"{program.name} {program.description or ''}".lower()
    keyword_hits = sum(1 for kw in keywords if kw in haystack)
    score += min(keyword_hits * KEYWORD_SCORE, MAX_KEYWORD_BONUS)

    return min(score, 100)


def map_niches_to_programmes(
    db_path: str = "data/affiliate_programs.db",
    niches_csv: str = "data/niches_export.csv",
    min_relevance: int = SECTOR_SCORE,
    top_n: int = 15,
) -> int:
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    niches = load_niches(niches_csv)
    print(f"Loaded {len(niches)} niches from {niches_csv}")

    # Preload active programmes once, grouped by relevant sector set, to
    # avoid one query per niche across 21k+ rows.
    programmes = session.query(AffiliateProgram).filter_by(is_active=1).all()
    print(f"Loaded {len(programmes)} active programmes")

    session.query(NicheProgramMapping).delete()

    total_mappings = 0
    unmatched_categories = set()

    for niche in niches:
        category = niche["parent_category"]
        sectors = CATEGORY_TO_SECTORS.get(category)
        if not sectors:
            unmatched_categories.add(category)
            continue

        keywords = niche_keywords(niche)
        scored = []
        for program in programmes:
            score = score_program(niche, keywords, program, sectors)
            if score >= min_relevance:
                scored.append((score, program))

        scored.sort(key=lambda x: x[0], reverse=True)

        for score, program in scored[:top_n]:
            mapping = NicheProgramMapping(
                niche_id=niche["niche_id"],
                niche_name=niche["name"],
                program_id=program.id,
                program_name=program.name,
                relevance_score=score,
                is_verified=0,
            )
            session.add(mapping)
            total_mappings += 1

    session.commit()
    session.close()

    print(f"\n✓ Created {total_mappings} niche-programme mappings")
    if unmatched_categories:
        print(f"⚠ No sector mapping defined for categories: {sorted(unmatched_categories)}")

    return total_mappings


def generate_mapping_report(db_path: str = "data/affiliate_programs.db", output_path: str = "data/NICHE_PROGRAM_MAPPING_REPORT.md"):
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    from sqlalchemy import func

    per_niche = (
        session.query(
            NicheProgramMapping.niche_name,
            func.count(NicheProgramMapping.id),
            func.avg(NicheProgramMapping.relevance_score),
        )
        .group_by(NicheProgramMapping.niche_name)
        .order_by(func.count(NicheProgramMapping.id).desc())
        .all()
    )

    total_niches_with_matches = len(per_niche)
    total_mappings = session.query(NicheProgramMapping).count()
    niches_without_matches_count = 0

    lines = [
        "# Niche → Programme Mapping Report",
        "",
        f"Total mappings: {total_mappings}",
        f"Niches with at least one matched programme: {total_niches_with_matches}",
        "",
        "| Niche | Matched Programmes | Avg Relevance |",
        "|---|---|---|",
    ]
    for niche_name, count, avg_score in per_niche:
        lines.append(f"| {niche_name} | {count} | {avg_score:.0f} |")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    session.close()
    print(f"✓ Report saved: {output_path}")


def main():
    stored = map_niches_to_programmes()
    if stored > 0:
        generate_mapping_report()
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())

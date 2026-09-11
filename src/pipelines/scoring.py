"""Provisional Opportunity Score and ranked niche shortlist.

The backlog's full formula is:
    25% RevenuePotential + 20% SearchDemand + 20% CommercialIntent
  + 20% SEOOpportunity  + 10% AffiliateQuality + 5% ContentFeasibility

RevenuePotential and SEOOpportunity can't be computed yet - Awin withholds
commission rates for unjoined programmes, and SERP analysis (Phase 4) needs a
paid API. The three computable components are renormalised to 100:

    40% SearchDemand + 40% CommercialIntent + 20% AffiliateQuality

Treat the output as a triage ranking, not a verdict. SEO difficulty is
unmeasured, so a high scorer may still be unrealistic to rank for.
"""

import argparse
import csv
import math
import sys
from datetime import datetime
from pathlib import Path

project_root = str(Path(__file__).resolve().parents[2])
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from src.models.phase2_db_models import NicheProgramMapping
from src.models.phase3_db_models import Base, KeywordDemand, NicheScore

WEIGHTS = {"search_demand": 0.40, "commercial_intent": 0.40, "affiliate_quality": 0.20}

# Winnability treats competition as a cost, not a signal of value. Caveat: Google's
# competition index measures *advertiser* competition for paid ads, not organic
# ranking difficulty. The two correlate but are not the same thing, so this is a
# proxy for SEO difficulty until real SERP analysis (Phase 4) replaces it.
WINNABILITY_WEIGHTS = {
    "search_demand": 0.30,
    "commercial_value": 0.25,
    "ease": 0.30,
    "affiliate_quality": 0.15,
}

# Rising/falling demand nudges the score; Trends' direction is directional only.
TREND_MODIFIER = {"rising": 6.0, "stable": 0.0, "falling": -6.0, "no_data": 0.0}

THRESHOLDS = [(70, "BUILD"), (55, "RESEARCH"), (40, "BACKLOG"), (0, "IGNORE")]


def percentile_ranks(values: list) -> list:
    """Rank-based percentile (0-100). Ties share the average rank, so the heavily
    bucketed Keyword Planner volumes produce honest plateaus rather than fake precision."""
    n = len(values)
    if n <= 1:
        return [50.0] * n

    indexed = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and values[indexed[j + 1]] == values[indexed[i]]:
            j += 1
        avg_rank = (i + j) / 2.0
        for k in range(i, j + 1):
            ranks[indexed[k]] = 100.0 * avg_rank / (n - 1)
        i = j + 1
    return ranks


def classify(score: float) -> str:
    for threshold, label in THRESHOLDS:
        if score >= threshold:
            return label
    return "IGNORE"


def load_inputs(session, niches_csv: str) -> list:
    niches = list(csv.DictReader(open(niches_csv, newline="", encoding="utf-8")))

    trends = {
        r.niche_id: r
        for r in session.query(KeywordDemand).filter_by(source="google_trends").all()
    }
    planner = {
        r.niche_id: r
        for r in session.query(KeywordDemand).filter_by(source="google_keyword_planner").all()
    }
    programs = {
        niche_id: (count, avg_rel)
        for niche_id, count, avg_rel in session.query(
            NicheProgramMapping.niche_id,
            func.count(NicheProgramMapping.id),
            func.avg(NicheProgramMapping.relevance_score),
        ).group_by(NicheProgramMapping.niche_id).all()
    }

    rows = []
    for niche in niches:
        nid = niche["niche_id"]
        t, p = trends.get(nid), planner.get(nid)
        count, avg_rel = programs.get(nid, (0, 0.0))
        rows.append({
            "niche_id": nid,
            "niche_name": niche["name"],
            "parent_category": niche["parent_category"],
            "volume": (p.search_volume_min if p and p.search_volume_min else 0),
            "trend_interest": (t.avg_interest if t and t.avg_interest else 0.0),
            "trend_direction": (t.trend_direction if t else "no_data"),
            "cpc_high": (p.cpc_high if p and p.cpc_high else 0.0),
            "competition_index": (p.competition_index if p and p.competition_index else 0),
            "program_count": count,
            "avg_relevance": float(avg_rel or 0.0),
        })
    return rows


def score_niches(rows: list) -> list:
    # log1p keeps the 10x volume buckets from dominating on a linear scale.
    vol_pct = percentile_ranks([math.log1p(r["volume"]) for r in rows])
    cpc_pct = percentile_ranks([r["cpc_high"] for r in rows])
    prog_pct = percentile_ranks([r["program_count"] for r in rows])

    for i, r in enumerate(rows):
        demand = 0.7 * vol_pct[i] + 0.3 * r["trend_interest"]
        demand = max(0.0, min(100.0, demand + TREND_MODIFIER.get(r["trend_direction"], 0.0)))

        # High competition means advertisers compete for the term - a signal of
        # commercial value here, not of SEO difficulty (that's unmeasured).
        intent = 0.65 * cpc_pct[i] + 0.35 * r["competition_index"]

        quality = 0.6 * prog_pct[i] + 0.4 * r["avg_relevance"]

        r["search_demand"] = round(demand, 1)
        r["commercial_intent"] = round(intent, 1)
        r["affiliate_quality"] = round(quality, 1)
        r["opportunity_score"] = round(
            WEIGHTS["search_demand"] * demand
            + WEIGHTS["commercial_intent"] * intent
            + WEIGHTS["affiliate_quality"] * quality,
            1,
        )
        r["recommendation"] = classify(r["opportunity_score"])

        # A niche with no volume data isn't "easy", it's unmeasured - don't let
        # a zero competition index reward it with a perfect ease score.
        ease = (100.0 - r["competition_index"]) if r["volume"] > 0 else 0.0
        r["ease"] = round(ease, 1)
        r["commercial_value"] = round(cpc_pct[i], 1)
        r["winnability_score"] = round(
            WINNABILITY_WEIGHTS["search_demand"] * demand
            + WINNABILITY_WEIGHTS["commercial_value"] * cpc_pct[i]
            + WINNABILITY_WEIGHTS["ease"] * ease
            + WINNABILITY_WEIGHTS["affiliate_quality"] * quality,
            1,
        )
        r["winnability_recommendation"] = classify(r["winnability_score"])

    rows.sort(key=lambda r: r["opportunity_score"], reverse=True)
    return rows


def store_scores(session, rows: list):
    session.query(NicheScore).delete()
    for r in rows:
        session.add(NicheScore(
            niche_id=r["niche_id"],
            niche_name=r["niche_name"],
            parent_category=r["parent_category"],
            search_demand=r["search_demand"],
            commercial_intent=r["commercial_intent"],
            affiliate_quality=r["affiliate_quality"],
            opportunity_score=r["opportunity_score"],
            recommendation=r["recommendation"],
            winnability_score=r["winnability_score"],
            winnability_recommendation=r["winnability_recommendation"],
            search_volume=r["volume"],
            trend_direction=r["trend_direction"],
            cpc_high=r["cpc_high"],
            competition_index=r["competition_index"],
            program_count=r["program_count"],
            scored_at=datetime.utcnow(),
        ))
    session.commit()


def write_report(rows: list, output_path: str):
    counts = {}
    for r in rows:
        counts[r["recommendation"]] = counts.get(r["recommendation"], 0) + 1

    lines = [
        "# Ranked Niche Shortlist - Provisional Opportunity Score",
        "",
        f"Generated: {datetime.now():%Y-%m-%d %H:%M} | Niches scored: {len(rows)}",
        "",
        "## Caveat",
        "",
        "This score is **provisional**. Two of the six components in the backlog's",
        "formula are missing: **RevenuePotential** (Awin withholds commission rates for",
        "unjoined programmes) and **SEOOpportunity** (needs Phase 4 SERP analysis via a",
        "paid API). The three computable components are renormalised to 100:",
        "",
        "> 40% SearchDemand + 40% CommercialIntent + 20% AffiliateQuality",
        "",
        "**SEO difficulty is unmeasured.** A niche can rank highly here and still be",
        "unrealistic to rank for in Google. Verify the top candidates before committing.",
        "",
        "Search volumes come from a no-spend Keyword Planner account, so they are",
        "bucketed (500 / 5.000 / 50.000 / 500.000 / 5.000.000) and indicate magnitude",
        "only. CPC and competition index are precise.",
        "",
        "## Summary",
        "",
        "| Recommendation | Count |",
        "|---|---|",
    ]
    for label in ["BUILD", "RESEARCH", "BACKLOG", "IGNORE"]:
        lines.append(f"| {label} | {counts.get(label, 0)} |")

    lines += [
        "",
        "## Ranked Niches",
        "",
        "| # | Niche | Category | Score | Demand | Intent | Affiliate | Volume | CPC high | Comp | Trend | Rec |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(rows, 1):
        lines.append(
            f"| {i} | {r['niche_name']} | {r['parent_category']} | **{r['opportunity_score']}** | "
            f"{r['search_demand']} | {r['commercial_intent']} | {r['affiliate_quality']} | "
            f"{r['volume']:,} | {r['cpc_high']:.2f} | {r['competition_index']} | "
            f"{r['trend_direction']} | {r['recommendation']} |"
        )

    Path(output_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✓ Report saved: {output_path}")


def write_winnability_report(rows: list, output_path: str):
    ranked = sorted(rows, key=lambda r: r["winnability_score"], reverse=True)

    lines = [
        "# Winnability Ranking - Where a New Site Could Realistically Compete",
        "",
        f"Generated: {datetime.now():%Y-%m-%d %H:%M} | Niches scored: {len(ranked)}",
        "",
        "## Why this exists",
        "",
        "The Opportunity Score in `NICHE_SHORTLIST.md` answers *where is the money*. It",
        "rewards high CPC and high competition, so its top entries are dominated by",
        "insurance, credit and energy comparison terms - exactly the niches owned by",
        "Check24, Verivox and similar. A new site cannot realistically rank there.",
        "",
        "This ranking answers a different question: *where could a new site actually win*.",
        "It treats competition as a cost:",
        "",
        "> 30% SearchDemand + 25% CommercialValue + 30% Ease + 15% AffiliateQuality",
        "",
        "## Important limitation",
        "",
        "**Ease is derived from Google's competition index, which measures competition",
        "among *advertisers bidding for paid ads* - not organic ranking difficulty.**",
        "The two correlate but are not the same. A term can have few advertisers and",
        "still have an immovable Wikipedia or Amazon result on page one. This is a proxy",
        "standing in for the Phase 4 SERP analysis, not a replacement for it.",
        "",
        "Niches with no volume data score 0 on Ease rather than 100 - unmeasured is not",
        "the same as easy.",
        "",
        "## Ranked Niches",
        "",
        "| # | Niche | Category | Winnability | Demand | Value | Ease | Affiliate | Volume | CPC high | Comp | Rec |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(ranked, 1):
        lines.append(
            f"| {i} | {r['niche_name']} | {r['parent_category']} | **{r['winnability_score']}** | "
            f"{r['search_demand']} | {r['commercial_value']} | {r['ease']} | {r['affiliate_quality']} | "
            f"{r['volume']:,} | {r['cpc_high']:.2f} | {r['competition_index']} | "
            f"{r['winnability_recommendation']} |"
        )

    Path(output_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✓ Report saved: {output_path}")


def write_csv(rows: list, output_path: str):
    cols = [
        "niche_id", "niche_name", "parent_category",
        "opportunity_score", "recommendation",
        "winnability_score", "winnability_recommendation",
        "search_demand", "commercial_intent", "affiliate_quality",
        "commercial_value", "ease",
        "volume", "cpc_high", "competition_index", "program_count", "trend_direction",
    ]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"✓ CSV saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Score and rank niches")
    parser.add_argument("--db", default="data/affiliate_programs.db")
    parser.add_argument("--niches", default="data/niches_export.csv")
    args = parser.parse_args()

    engine = create_engine(f"sqlite:///{args.db}", echo=False)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    rows = load_inputs(session, args.niches)
    rows = score_niches(rows)
    store_scores(session, rows)
    session.close()

    write_report(rows, "data/NICHE_SHORTLIST.md")
    write_winnability_report(rows, "data/NICHE_WINNABILITY.md")
    write_csv(rows, "data/niche_shortlist.csv")

    counts = {}
    for r in rows:
        counts[r["recommendation"]] = counts.get(r["recommendation"], 0) + 1
    print(f"\n✓ Scored {len(rows)} niches: " + ", ".join(f"{k}={v}" for k, v in counts.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Niche discovery and generation from seed data."""

import json
import re
import unicodedata
from pathlib import Path
from datetime import datetime
from typing import Optional

from pydantic import ValidationError

from src.models.niche import NicheCreate, Niche


def slugify(text: str) -> str:
    """Convert text to URL-safe slug."""
    # Normalize unicode
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    # Convert to lowercase and replace spaces/special chars
    text = re.sub(r"[^\w\s-]", "", text).strip()
    text = re.sub(r"[-\s]+", "-", text)
    return text.lower()


def load_niche_seeds(yaml_path: str | Path) -> dict:
    """Load niche seed categories from YAML."""
    import yaml

    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    return data


def generate_niches_from_seeds(categories_data: dict) -> list[Niche]:
    """Generate niche records from seed categories."""
    niches = []

    for category_key, category_info in categories_data["categories"].items():
        category_name = category_info["name"]
        category_description = category_info["description"]
        niche_names = category_info.get("niches", [])

        for niche_name in niche_names:
            niche_id = slugify(f"{category_key}_{niche_name}")

            try:
                niche = Niche(
                    niche_id=niche_id,
                    name=niche_name,
                    parent_category=category_name,
                    description=category_description,
                    language="de",
                    country="DE",
                    seed_keywords=[niche_name.lower()],
                    candidate_source="affiliate_categories",
                    status="candidate",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                niches.append(niche)
            except ValidationError as e:
                print(f"Warning: Failed to create niche {niche_name}: {e}")
                continue

    return niches


def export_niches_csv(niches: list[Niche], output_path: str | Path) -> None:
    """Export niches to CSV for manual review."""
    import csv

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "niche_id",
                "name",
                "parent_category",
                "description",
                "language",
                "country",
                "status",
                "created_at",
            ],
        )
        writer.writeheader()
        for niche in sorted(niches, key=lambda n: n.parent_category):
            writer.writerow(
                {
                    "niche_id": niche.niche_id,
                    "name": niche.name,
                    "parent_category": niche.parent_category,
                    "description": niche.description,
                    "language": niche.language,
                    "country": niche.country,
                    "status": niche.status,
                    "created_at": niche.created_at.isoformat(),
                }
            )


def export_niches_json(niches: list[Niche], output_path: str | Path) -> None:
    """Export niches to JSON for database import."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = [niche.model_dump(mode="json") for niche in niches]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)


def generate_niche_report(niches: list[Niche]) -> str:
    """Generate a summary report of generated niches."""
    categories = {}
    for niche in niches:
        cat = niche.parent_category
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(niche.name)

    report = []
    report.append(f"# Niche Generation Report")
    report.append(f"\n**Total Niches Generated:** {len(niches)}")
    report.append(f"**Language:** German (de)")
    report.append(f"**Country:** Germany (DE)")
    report.append(f"**Generated:** {datetime.utcnow().isoformat()}\n")

    report.append("## By Category\n")
    for cat in sorted(categories.keys()):
        niches_in_cat = categories[cat]
        report.append(f"### {cat} ({len(niches_in_cat)})\n")
        for niche in sorted(niches_in_cat):
            report.append(f"- {niche}\n")

    return "".join(report)


def main(
    yaml_path: str | Path = "config/niches.yaml",
    output_dir: str | Path = "data",
    generate_csv: bool = True,
    generate_json: bool = True,
    generate_report: bool = True,
) -> list[Niche]:
    """Main niche generation pipeline."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading niche seeds from {yaml_path}...")
    categories = load_niche_seeds(yaml_path)

    print("Generating niches...")
    niches = generate_niches_from_seeds(categories)
    print(f"✓ Generated {len(niches)} niches")

    if generate_csv:
        csv_path = output_dir / "niches_export.csv"
        export_niches_csv(niches, csv_path)
        print(f"✓ Exported to {csv_path}")

    if generate_json:
        json_path = output_dir / "niches_export.json"
        export_niches_json(niches, json_path)
        print(f"✓ Exported to {json_path}")

    if generate_report:
        report_path = output_dir / "NICHE_GENERATION_REPORT.md"
        report = generate_niche_report(niches)
        with open(report_path, "w") as f:
            f.write(report)
        print(f"✓ Report generated at {report_path}")

    return niches


if __name__ == "__main__":
    main()

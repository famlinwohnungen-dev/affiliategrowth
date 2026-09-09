#!/usr/bin/env python
"""Main entry point for niche generation."""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.chdir(project_root)

from src.pipelines.niche_discovery import main as generate_niches


def main():
    """Run niche generation pipeline."""
    print("=" * 60)
    print("AFFILIATE INTELLIGENCE MVP")
    print("Phase 1: Niche Generation")
    print("=" * 60)
    print()

    try:
        niches = generate_niches(
            yaml_path="config/niches.yaml",
            output_dir="data",
            generate_csv=True,
            generate_json=True,
            generate_report=True,
        )

        print()
        print("=" * 60)
        print(f"SUCCESS: {len(niches)} niches generated and exported")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Review data/NICHE_GENERATION_REPORT.md")
        print("2. Review data/niches_export.csv")
        print("3. Check data/niches_export.json for import")
        print()
        print("Ready for Phase 2: Affiliate Program Discovery")

    except Exception as e:
        print()
        print("=" * 60)
        print(f"ERROR: {e}")
        print("=" * 60)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

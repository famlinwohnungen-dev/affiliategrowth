"""Awin Publisher API collector for affiliate programmes."""

import os
import requests
import json
from datetime import datetime
from typing import List, Dict, Optional


class AwinCollector:
    """Fetch affiliate programmes from Awin Publisher API."""

    BASE_URL = "https://api.awin.com"

    def __init__(self, token: str, publisher_id: int):
        """
        Initialize Awin collector.

        Args:
            token: Awin API Bearer token
            publisher_id: Awin publisher ID (numeric)
        """
        self.token = token
        self.publisher_id = publisher_id
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }

    def get_available_programmes(self, limit: int = 500, offset: int = 0) -> List[Dict]:
        """
        Fetch available programmes for publisher.

        Args:
            limit: Number of programmes to fetch per request
            offset: Pagination offset

        Returns:
            List of programme dictionaries
        """
        url = f"{self.BASE_URL}/publishers/{self.publisher_id}/programmes"
        params = {
            "relationship": "notjoined",
            "limit": limit,
            "offset": offset,
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()

            programmes = response.json()
            if isinstance(programmes, list):
                return programmes
            return []

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching Awin programmes: {e}")
            return []

    def get_joined_programmes(self, limit: int = 500, offset: int = 0) -> List[Dict]:
        """
        Fetch programmes you've already joined.

        Args:
            limit: Number of programmes to fetch per request
            offset: Pagination offset

        Returns:
            List of programme dictionaries
        """
        url = f"{self.BASE_URL}/publishers/{self.publisher_id}/programmes"
        params = {
            "relationship": "joined",
            "limit": limit,
            "offset": offset,
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()

            programmes = response.json()
            if isinstance(programmes, list):
                return programmes
            return []

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching joined programmes: {e}")
            return []

    def parse_programme(self, raw_programme: Dict) -> Dict:
        """
        Parse raw Awin programme data into normalized format.

        Args:
            raw_programme: Raw JSON from Awin API

        Returns:
            Normalized programme dictionary
        """
        return {
            "source": "awin",
            "program_id": str(raw_programme.get("id", "")),
            "name": raw_programme.get("name", ""),
            "description": raw_programme.get("description", ""),
            "website": raw_programme.get("websiteUrl", ""),
            "support_url": raw_programme.get("supportUrl", ""),
            "is_active": 1 if raw_programme.get("status") == "active" else 0,
            "country": raw_programme.get("country", "DE"),
            "language": raw_programme.get("language", "de"),
            "raw_data": raw_programme,  # Store raw for reference
            "fetched_at": datetime.utcnow().isoformat(),
        }

    def fetch_all_available(self, batch_size: int = 500) -> List[Dict]:
        """
        Fetch all available programmes with pagination.

        Args:
            batch_size: How many to fetch per request

        Returns:
            List of all available programmes
        """
        all_programmes = []
        offset = 0

        print("Fetching available programmes from Awin...")

        while True:
            batch = self.get_available_programmes(limit=batch_size, offset=offset)

            if not batch:
                break

            print(f"  Fetched {len(batch)} programmes (offset: {offset})")
            all_programmes.extend(batch)

            # Stop if we got fewer than batch_size (last page)
            if len(batch) < batch_size:
                break

            offset += batch_size

        print(f"✓ Total programmes fetched: {len(all_programmes)}")
        return all_programmes

    def save_raw_data(self, programmes: List[Dict], output_path: str = "data/awin_raw.json"):
        """Save raw programme data for inspection."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(programmes, f, indent=2, default=str)

        print(f"✓ Saved raw data: {output_path}")


def main():
    """Test Awin collector."""
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    token = os.getenv("AWIN_TOKEN")
    publisher_id = int(os.getenv("AWIN_PUBLISHER_ID", 0))

    if not token or not publisher_id:
        print("❌ AWIN_TOKEN and AWIN_PUBLISHER_ID must be set in .env")
        return False

    print("=" * 60)
    print("AWIN COLLECTOR TEST")
    print("=" * 60)
    print(f"Publisher ID: {publisher_id}")
    print()

    collector = AwinCollector(token=token, publisher_id=publisher_id)

    # Fetch available programmes
    programmes = collector.fetch_all_available(batch_size=100)

    if programmes:
        # Parse first few
        print(f"\nSample programme (first of {len(programmes)}):")
        parsed = collector.parse_programme(programmes[0])
        print(json.dumps(parsed, indent=2, default=str))

        # Save raw data
        collector.save_raw_data(programmes)

        print("\n" + "=" * 60)
        print(f"✅ SUCCESS: {len(programmes)} programmes fetched and saved")
        print("=" * 60)
        return True
    else:
        print("\n❌ No programmes fetched")
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)

"""SQLAlchemy database models for Phase 2: Affiliate Program Discovery."""

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
            "relationship": "available",
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

            if len(batch) < batch_size:
                break

            offset += batch_size

        print(f"✓ Total programmes fetched: {len(all_programmes)}")
        return all_programmes

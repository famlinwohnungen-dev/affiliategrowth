"""Awin Publisher API collector for affiliate programmes."""

import os
import requests
import json
from datetime import datetime
from typing import List, Dict


class AwinCollector:
    """Fetch affiliate programmes from Awin Publisher API."""

    BASE_URL = "https://api.awin.com"

    def __init__(self, token: str, publisher_id: int):
        """Initialize Awin collector."""
        self.token = token
        self.publisher_id = publisher_id
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }

    def get_available_programmes(self) -> List[Dict]:
        """Fetch available (not-yet-joined) programmes for publisher.

        The Awin API does not accept 'available' as a relationship value.
        Valid values are: joined, pending, suspended, rejected, notjoined.
        'notjoined' is the closest match to "available to apply to".
        """
        url = f"{self.BASE_URL}/publishers/{self.publisher_id}/programmes"
        params = {
            "relationship": "notjoined",
        }

        try:
            print(f"Requesting: {url}")
            print(f"Params: {params}")
            response = requests.get(url, headers=self.headers, params=params, timeout=10)

            print(f"Status: {response.status_code}")

            if response.status_code != 200:
                print(f"Response: {response.text}")
                response.raise_for_status()

            programmes = response.json()
            if isinstance(programmes, list):
                return programmes
            return []
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching Awin programmes: {e}")
            return []

    def fetch_all_available(self) -> List[Dict]:
        """Fetch all available programmes."""
        print("Fetching available programmes from Awin...")
        programmes = self.get_available_programmes()
        print(f"✓ Total programmes fetched: {len(programmes)}")
        return programmes

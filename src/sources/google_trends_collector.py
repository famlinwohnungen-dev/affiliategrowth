"""Google Trends collector for keyword demand signals (free, no account needed).

Uses the unofficial `pytrends` client. Google Trends only gives relative
interest (0-100 over the requested window, per keyword batch), not absolute
search volume - this is a directional signal to triage niches before paying
for a commercial provider (DataForSEO, SerpApi, etc.) on the shortlist.

Google aggressively rate-limits this unofficial endpoint from datacenter
IPs, so requests are paced with a delay between them.
"""

import time
from typing import Dict, List, Optional

from pytrends.request import TrendReq


class GoogleTrendsCollector:
    """Fetch relative search-interest trends from Google Trends."""

    def __init__(self, geo: str = "DE", hl: str = "de-DE", request_delay: float = 15.0):
        """
        Args:
            geo: Country code to scope trends to.
            hl: Locale for the Trends UI/response.
            request_delay: Seconds to sleep between requests to avoid 429s.
        """
        self.geo = geo
        self.request_delay = request_delay
        self.client = TrendReq(hl=hl, tz=60)

    def get_keyword_interest(self, keyword: str, timeframe: str = "today 12-m") -> Optional[Dict]:
        """
        Fetch interest-over-time for a single keyword.

        Returns:
            Dict with avg_interest, latest_interest, trend_direction,
            or None if the request failed.
        """
        try:
            self.client.build_payload([keyword], geo=self.geo, timeframe=timeframe)
            df = self.client.interest_over_time()

            if df.empty or keyword not in df.columns:
                return {
                    "keyword": keyword,
                    "avg_interest": 0.0,
                    "latest_interest": 0.0,
                    "trend_direction": "no_data",
                }

            series = df[keyword]
            avg_interest = float(series.mean())
            latest_interest = float(series.iloc[-1])
            first_interest = float(series.iloc[0])

            if latest_interest > first_interest * 1.15:
                direction = "rising"
            elif latest_interest < first_interest * 0.85:
                direction = "falling"
            else:
                direction = "stable"

            return {
                "keyword": keyword,
                "avg_interest": avg_interest,
                "latest_interest": latest_interest,
                "trend_direction": direction,
            }

        except Exception as e:
            print(f"  ⚠ Trends error for '{keyword}': {e}")
            return None

    def fetch_batch(self, keywords: List[str], timeframe: str = "today 12-m") -> List[Dict]:
        """Fetch interest for multiple keywords, one request at a time with pacing."""
        results = []
        for i, keyword in enumerate(keywords):
            print(f"  [{i + 1}/{len(keywords)}] Fetching trends for '{keyword}'...")
            result = self.get_keyword_interest(keyword, timeframe=timeframe)
            if result:
                results.append(result)

            if i < len(keywords) - 1:
                time.sleep(self.request_delay)

        return results

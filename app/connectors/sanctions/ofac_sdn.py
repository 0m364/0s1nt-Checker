import csv
import os
import time
import requests
from typing import List
from app.connectors.base import BaseConnector
from app.connectors.utils import name_match_score
from app.schemas import PersonSearch, SearchResult

class OFACSDNConnector(BaseConnector):
    name = "OFAC SDN"
    source_type = "sanctions"
    url = "https://ofac.treasury.gov/media/tdf/sdn.csv"
    cache_path = "data/ofac_sdn.csv"
    cache_ttl = 86400

    def _download_if_needed(self):
        try:
            os.makedirs("data", exist_ok=True)
            if os.path.exists(self.cache_path):
                age = time.time() - os.path.getmtime(self.cache_path)
                if age < self.cache_ttl:
                    return
            r = requests.get(self.url, timeout=20)
            r.raise_for_status()
            with open(self.cache_path, "wb") as f:
                f.write(r.content)
        except Exception:
            pass

    def search(self, person: PersonSearch) -> List[SearchResult]:
        full_name = person.full_name
        if not full_name:
            return []

        self._download_if_needed()
        if not os.path.exists(self.cache_path):
            return []

        results = []
        try:
            with open(self.cache_path, newline="", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    record_name = row.get("name", "") or row.get("Name", "")
                    if not record_name:
                        continue

                    score = name_match_score(full_name, record_name)
                    if score < 0.6:
                        continue

                    record_id = row.get("uid") or row.get("Unique ID")

                    results.append(SearchResult(
                        source_name=self.name,
                        source_type=self.source_type,
                        record_id=record_id,
                        evidence_url="https://ofac.treasury.gov/sanctions-list-service",
                        raw_json=row,
                        confidence_score=score
                    ))
        except Exception:
            pass

        return results

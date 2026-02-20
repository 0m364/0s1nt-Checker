import csv
import os
import time
import requests
from connectors.base import BaseConnector
from connectors.utils import name_match_score

class OFACSDNConnector(BaseConnector):
    name = "OFAC SDN"
    source_type = "sanctions"
    url = "https://ofac.treasury.gov/media/tdf/sdn.csv"
    cache_path = "data/ofac_sdn.csv"
    cache_ttl = 86400

    def _download_if_needed(self):
        os.makedirs("data", exist_ok=True)
        if os.path.exists(self.cache_path):
            age = time.time() - os.path.getmtime(self.cache_path)
            if age < self.cache_ttl:
                return
        r = requests.get(self.url, timeout=20)
        r.raise_for_status()
        with open(self.cache_path, "wb") as f:
            f.write(r.content)

    def search(self, person: dict):
        full_name = person.get("full_name", "")
        if not full_name:
            return []
        self._download_if_needed()
        results = []
        with open(self.cache_path, newline="", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                record_name = row.get("name", "") or row.get("Name", "")
                score = name_match_score(full_name, record_name)
                if score < 0.6:
                    continue
                results.append({
                    "source_name": self.name,
                    "source_type": self.source_type,
                    "record_id": row.get("uid") or row.get("Unique ID"),
                    "evidence_url": "https://ofac.treasury.gov/sanctions-list-service",
                    "raw_json": row,
                    "confidence_score": score
                })
        return results

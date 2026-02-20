import requests
from connectors.base import BaseConnector
from connectors.utils import name_match_score

class FBIMostWantedConnector(BaseConnector):
    name = "FBI Most Wanted"
    source_type = "wanted"
    base_url = "https://api.fbi.gov/@wanted"

    def search(self, person: dict):
        full_name = person.get("full_name", "")
        if not full_name:
            return []
        params = {"title": full_name}
        resp = requests.get(self.base_url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        results = []
        for item in data.get("items", []):
            record_name = item.get("title") or ""
            score = name_match_score(full_name, record_name)
            if score < 0.6:
                continue
            results.append({
                "source_name": self.name,
                "source_type": self.source_type,
                "record_id": item.get("uid"),
                "evidence_url": item.get("url"),
                "raw_json": item,
                "confidence_score": score
            })
        return results

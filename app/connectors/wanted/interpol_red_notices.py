import requests
from connectors.base import BaseConnector
from connectors.utils import name_match_score

class InterpolRedNoticesConnector(BaseConnector):
    name = "Interpol Red Notices"
    source_type = "wanted"
    base_url = "https://ws-public.interpol.int/notices/v1/red"

    def search(self, person: dict):
        full_name = person.get("full_name", "")
        if not full_name:
            return []
        params = {"name": full_name}
        resp = requests.get(self.base_url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        results = []
        for item in data.get("_embedded", {}).get("notices", []):
            record_name = " ".join(filter(None, [item.get("forename"), item.get("name")]))
            score = name_match_score(full_name, record_name)
            if score < 0.6:
                continue
            results.append({
                "source_name": self.name,
                "source_type": self.source_type,
                "record_id": item.get("entity_id"),
                "evidence_url": item.get("_links", {}).get("self", {}).get("href"),
                "raw_json": item,
                "confidence_score": score
            })
        return results

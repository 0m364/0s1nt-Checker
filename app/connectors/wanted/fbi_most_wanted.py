import requests
from typing import List
from app.connectors.base import BaseConnector
from app.connectors.utils import name_match_score
from app.schemas import PersonSearch, SearchResult

class FBIMostWantedConnector(BaseConnector):
    name = "FBI Most Wanted"
    source_type = "wanted"
    base_url = "https://api.fbi.gov/@wanted"

    def search(self, person: PersonSearch) -> List[SearchResult]:
        full_name = person.full_name
        if not full_name:
            return []

        params = {"title": full_name}
        try:
            resp = requests.get(self.base_url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            results = []
            for item in data.get("items", []):
                record_name = item.get("title", "") or ""
                if not record_name:
                    continue
                score = name_match_score(full_name, record_name)
                if score < 0.6:
                    continue

                record_id = item.get("uid")
                evidence_url = item.get("url")

                results.append(SearchResult(
                    source_name=self.name,
                    source_type=self.source_type,
                    record_id=record_id,
                    evidence_url=evidence_url,
                    raw_json=item,
                    confidence_score=score
                ))
            return results
        except Exception:
            return []

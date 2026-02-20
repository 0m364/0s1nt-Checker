import requests
from typing import List
from app.connectors.base import BaseConnector
from app.connectors.utils import name_match_score
from app.schemas import PersonSearch, SearchResult

class InterpolRedNoticesConnector(BaseConnector):
    name = "Interpol Red Notices"
    source_type = "wanted"
    base_url = "https://ws-public.interpol.int/notices/v1/red"

    def search(self, person: PersonSearch) -> List[SearchResult]:
        full_name = person.full_name
        if not full_name:
            return []

        params = {"name": full_name}
        try:
            resp = requests.get(self.base_url, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()

            results = []
            for item in data.get("_embedded", {}).get("notices", []):
                forename = item.get("forename")
                name = item.get("name")
                record_name = " ".join(filter(None, [forename, name]))

                if not record_name:
                    continue

                score = name_match_score(full_name, record_name)
                if score < 0.6:
                    continue

                entity_id = item.get("entity_id")
                evidence_url = item.get("_links", {}).get("self", {}).get("href")

                results.append(SearchResult(
                    source_name=self.name,
                    source_type=self.source_type,
                    record_id=entity_id,
                    evidence_url=evidence_url,
                    raw_json=item,
                    confidence_score=score
                ))
            return results
        except Exception:
            return []

from typing import List
from app.connectors.base import BaseConnector
from app.schemas import PersonSearch, SearchResult

class NSOPWConnector(BaseConnector):
    name = "NSOPW"
    source_type = "registry"

    def search(self, person: PersonSearch) -> List[SearchResult]:
        # Implement only via official public endpoints per ToS.
        return []

from abc import ABC, abstractmethod
from typing import List
from app.schemas import PersonSearch, SearchResult

class BaseConnector(ABC):
    """
    Abstract base class for all data connectors.
    """
    name: str
    source_type: str
    terms_url: str = ""
    rate_limit: str = ""
    cache_ttl_seconds: int = 86400
    attribution: str = ""

    @abstractmethod
    def search(self, person: PersonSearch) -> List[SearchResult]:
        """
        Search the connector for the given person.

        Args:
            person: PersonSearch object containing search criteria.

        Returns:
            List of SearchResult objects.
        """
        raise NotImplementedError

from abc import ABC, abstractmethod

class BaseConnector(ABC):
    name: str
    source_type: str
    terms_url: str = ""
    rate_limit: str = ""
    cache_ttl_seconds: int = 86400
    attribution: str = ""

    @abstractmethod
    def search(self, person: dict):
        raise NotImplementedError

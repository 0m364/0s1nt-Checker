from connectors.base import BaseConnector

class NSOPWConnector(BaseConnector):
    name = "NSOPW"
    source_type = "registry"

    def search(self, person: dict):
        # Implement only via official public endpoints per ToS.
        return []

from app.core.config import settings
from app.connectors.wanted.fbi_most_wanted import FBIMostWantedConnector
from app.connectors.sanctions.ofac_sdn import OFACSDNConnector
from app.connectors.wanted.interpol_red_notices import InterpolRedNoticesConnector
from app.connectors.registries.nsopw import NSOPWConnector

def get_all_connectors():
    connectors = []
    if settings.sources.fbi_most_wanted:
        connectors.append(FBIMostWantedConnector())
    if settings.sources.ofac_sdn:
        connectors.append(OFACSDNConnector())
    if settings.sources.interpol_red_notices:
        connectors.append(InterpolRedNoticesConnector())
    if settings.sources.nsopw:
        connectors.append(NSOPWConnector())
    return connectors

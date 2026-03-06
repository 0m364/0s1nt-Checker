from app.core.config import settings
from app.connectors.wanted.fbi_most_wanted import FBIMostWantedConnector
from app.connectors.sanctions.ofac_sdn import OFACSDNConnector
from app.connectors.wanted.interpol_red_notices import InterpolRedNoticesConnector
from app.connectors.registries.nsopw import NSOPWConnector
from app.connectors.factbook.cia_factbook import CIAFactbookConnector

def get_all_connectors():
    connectors = []
    if getattr(settings.sources, 'fbi_most_wanted', False):
        connectors.append(FBIMostWantedConnector())
    if getattr(settings.sources, 'ofac_sdn', False):
        connectors.append(OFACSDNConnector())
    if getattr(settings.sources, 'interpol_red_notices', False):
        connectors.append(InterpolRedNoticesConnector())
    if getattr(settings.sources, 'nsopw', False):
        connectors.append(NSOPWConnector())
    if getattr(settings.sources, 'cia_factbook', False):
        connectors.append(CIAFactbookConnector())
    return connectors

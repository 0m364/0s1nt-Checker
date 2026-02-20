from app.config import load_config
from connectors.wanted.fbi_most_wanted import FBIMostWantedConnector
from connectors.sanctions.ofac_sdn import OFACSDNConnector
from connectors.wanted.interpol_red_notices import InterpolRedNoticesConnector
from connectors.registries.nsopw import NSOPWConnector

def get_all_connectors():
    cfg = load_config()
    connectors = []
    if cfg["sources"].get("fbi_most_wanted"):
        connectors.append(FBIMostWantedConnector())
    if cfg["sources"].get("ofac_sdn"):
        connectors.append(OFACSDNConnector())
    if cfg["sources"].get("interpol_red_notices"):
        connectors.append(InterpolRedNoticesConnector())
    if cfg["sources"].get("nsopw"):
        connectors.append(NSOPWConnector())
    return connectors

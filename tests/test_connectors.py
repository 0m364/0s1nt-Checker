from app.connectors.utils import normalize_name, name_match_score
from app.connectors.registries.nsopw import NSOPWConnector

def test_normalize_name():
    assert normalize_name("John Doe") == "john doe"
    assert normalize_name("John   Doe") == "john doe"
    assert normalize_name("John-Doe") == "johndoe"
    assert normalize_name("O'Connor") == "oconnor"
    assert normalize_name("Björk") == "bjrk" # regex only keeps a-z0-9

def test_name_match_score():
    assert name_match_score("John Doe", "John Doe") == 0.95
    assert name_match_score("John Doe", "john doe") == 0.95
    assert name_match_score("John Doe", "John P. Doe") > 0.0
    assert name_match_score("John Doe", "Jane Doe") == 0.0 # simple fuzzy

def test_nsopw_connector(person_search):
    connector = NSOPWConnector()
    results = connector.search(person_search)
    assert isinstance(results, list)
    assert len(results) == 0

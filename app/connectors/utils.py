import re

def normalize_name(name: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", name.lower()).strip()


def name_match_score(person_name: str, record_name: str) -> float:
    p = normalize_name(person_name)
    r = normalize_name(record_name)
    if p == r:
        return 0.95
    if p in r or r in p:
        return 0.75
    return 0.0

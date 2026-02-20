import re

def normalize_name(name: str) -> str:
    """
    Normalize a name string by removing non-alphanumeric characters and lowercasing.

    Args:
        name: The name string to normalize.

    Returns:
        The normalized name string.
    """
    if not name:
        return ""
    # Remove non-alphanumeric characters except spaces
    cleaned = re.sub(r"[^a-z0-9 ]", "", name.lower()).strip()
    # Replace multiple spaces with single space
    return re.sub(r"\s+", " ", cleaned)


def name_match_score(person_name: str, record_name: str) -> float:
    """
    Calculate a similarity score between two names.

    Args:
        person_name: The name of the person being searched.
        record_name: The name of the record found.

    Returns:
        A float between 0.0 and 1.0 representing the similarity score.
    """
    p = normalize_name(person_name)
    r = normalize_name(record_name)

    if not p or not r:
        return 0.0

    if p == r:
        return 0.95
    if p in r or r in p:
        return 0.75

    # Improve matching: check for token overlap
    p_tokens = set(p.split())
    r_tokens = set(r.split())

    if not p_tokens or not r_tokens:
        return 0.0

    intersection = p_tokens.intersection(r_tokens)
    union = p_tokens.union(r_tokens)

    jaccard = len(intersection) / len(union)

    if jaccard > 0.5:
        return 0.5 + (jaccard * 0.4) # scale to 0.5 - 0.9 range

    return 0.0

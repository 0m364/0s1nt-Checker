def dedup_evidence(evidence_list):
    seen = set()
    unique = []
    for e in evidence_list:
        key = (e.get("source_name"), e.get("record_id"), e.get("evidence_url"))
        if key in seen:
            continue
        seen.add(key)
        unique.append(e)
    return unique

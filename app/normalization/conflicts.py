def detect_conflicts(evidence_records):
    conflicts = []
    dobs = set()
    addresses = set()

    for e in evidence_records:
        raw = e.raw_json or {}
        if raw.get("dob"):
            dobs.add(raw.get("dob"))
        if raw.get("address"):
            addresses.add(raw.get("address"))

    if len(dobs) > 1:
        conflicts.append("Multiple DOBs found across sources.")
    if len(addresses) > 1:
        conflicts.append("Multiple addresses found across sources.")

    tiers = {e.match_tier for e in evidence_records}
    if "A" in tiers and ("C" in tiers or "D" in tiers):
        conflicts.append("High-confidence match mixed with low-confidence matches.")

    return conflicts

def compute_match_tier(person: dict, record: dict) -> str:
    has_name = bool(person.get("full_name") and record.get("full_name"))
    has_dob = bool(person.get("dob") and record.get("dob"))
    has_addr = bool(person.get("address") and record.get("address"))
    has_phone = bool(person.get("phone") and record.get("phone"))

    if has_name and has_dob and (has_addr or has_phone):
        return "A"
    if has_name and has_dob:
        return "B"
    if has_name and has_addr:
        return "C"
    if has_name:
        return "D"
    return "D"

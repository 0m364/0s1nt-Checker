def score_case(evidence_list: list) -> dict:
    computed_score = 1
    confidence_tier = "D"
    rationale = "No indicators."

    tiers = [e["match_tier"] for e in evidence_list]
    if "A" in tiers:
        confidence_tier = "A"
    elif "B" in tiers:
        confidence_tier = "B"
    elif "C" in tiers:
        confidence_tier = "C"
    elif "D" in tiers:
        confidence_tier = "D"

    if confidence_tier in ["C", "D"]:
        return {
            "computed_score": 1,
            "confidence_tier": confidence_tier,
            "rationale": "Low-confidence matches only; manual review required."
        }

    if any(e["source_type"] == "wanted" and e["match_tier"] in ["A", "B"] for e in evidence_list):
        computed_score = 5
        rationale = "Official wanted list match."
    elif any(e["source_type"] == "registry" and e["match_tier"] in ["A", "B"] for e in evidence_list):
        computed_score = 4
        rationale = "Public registry or watchlist match."
    elif any(e["source_type"] in ["court", "media"] for e in evidence_list):
        computed_score = 3
        rationale = "Adverse media or court record match."
    elif any(e["source_type"] == "social" for e in evidence_list):
        computed_score = 2
        rationale = "Public social threats or extremist content."

    return {
        "computed_score": computed_score,
        "confidence_tier": confidence_tier,
        "rationale": rationale
    }

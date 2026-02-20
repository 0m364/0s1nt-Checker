def build_explainability(score_data, evidence):
    reasons = []
    for e in evidence:
        reasons.append({
            "source": e.source_name,
            "type": e.source_type,
            "match_tier": e.match_tier,
            "confidence": float(e.confidence_score),
            "reason": f"Matched {e.source_type} source at tier {e.match_tier}"
        })

    summary = (
        f"Score {score_data['computed_score']} assigned because "
        f"{score_data['rationale']}. "
        f"Confidence tier: {score_data['confidence_tier']}."
    )

    return {"summary": summary, "evidence_reasons": reasons}

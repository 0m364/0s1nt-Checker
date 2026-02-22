def build_explainability(score_data, evidence):
    reasons = []
    for e in evidence:
        # Handle dict (new format) or object (old format attempt)
        if isinstance(e, dict):
            source_name = e.get("source_name")
            source_type = e.get("source_type")
            match_tier = e.get("match_tier")
            confidence_score = e.get("confidence_score")
        else:
            # Fallback for object access if needed
            source_name = getattr(e, "source_name", "Unknown")
            source_type = getattr(e, "source_type", "Unknown")
            match_tier = getattr(e, "match_tier", "Unknown")
            confidence_score = getattr(e, "confidence_score", 0.0)

        reasons.append({
            "source": source_name,
            "type": source_type,
            "match_tier": match_tier,
            "confidence": float(confidence_score) if confidence_score is not None else 0.0,
            "reason": f"Matched {source_type} source at tier {match_tier}"
        })

    summary = (
        f"Score {score_data['computed_score']} assigned because "
        f"{score_data['rationale']}. "
        f"Confidence tier: {score_data['confidence_tier']}."
    )

    return {"summary": summary, "evidence_reasons": reasons}

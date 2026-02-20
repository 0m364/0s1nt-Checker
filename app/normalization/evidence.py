def normalize_evidence(rec: dict) -> dict:
    return {
        "source_name": rec.get("source_name", ""),
        "source_type": rec.get("source_type", ""),
        "record_id": rec.get("record_id"),
        "evidence_url": rec.get("evidence_url"),
        "raw_json": rec.get("raw_json", {}),
        "confidence_score": float(rec.get("confidence_score", 0.0)),
        "match_notes": rec.get("match_notes", "")
    }

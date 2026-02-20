from app.connectors.registry import get_all_connectors
from app.scoring.match_tier import compute_match_tier
from app.scoring.engine import score_case
from app.scoring.explainability import build_explainability
from app.normalization.evidence import normalize_evidence
from app.normalization.dedup import dedup_evidence
from app.normalization.conflicts import detect_conflicts
from app import models
from app.db import SessionLocal
from app.schemas import PersonSearch

def run_case_pipeline(_, case_id: str):
    db = SessionLocal()
    try:
        case = db.query(models.Case).get(case_id)
        if not case:
            return

        person = db.query(models.Person).get(case.person_id)
        if not person:
            return

        person_search = PersonSearch(
            full_name=person.full_name,
            dob=str(person.dob) if person.dob else None,
            address=person.address,
            email=person.email,
            phone=person.phone
        )

        # Keep person_dict for scoring logic if needed, or update scoring logic too.
        # compute_match_tier(person_dict, rec) uses person_dict.
        person_dict = {
            "full_name": person.full_name,
            "dob": person.dob,
            "address": person.address,
            "email": person.email,
            "phone": person.phone
        }

        evidence_list = []

        for connector in get_all_connectors():
            # Connector returns List[SearchResult]
            search_results = connector.search(person_search)

            # Convert to dict for existing pipeline logic
            results_dicts = [r.model_dump() for r in search_results]

            normalized_results = [normalize_evidence(r) for r in results_dicts]
            deduped_results = dedup_evidence(normalized_results)

            for rec in deduped_results:
                e = models.Evidence(
                    case_id=case_id,
                    source_name=rec["source_name"],
                    source_type=rec["source_type"],
                    record_id=rec.get("record_id"),
                    evidence_url=rec.get("evidence_url"),
                    raw_json=rec.get("raw_json")
                )
                db.add(e)
                db.flush()

                tier = compute_match_tier(person_dict, rec)
                confidence = rec.get("confidence_score", 0.5)

                m = models.Match(
                    case_id=case_id,
                    evidence_id=e.id,
                    match_tier=tier,
                    confidence_score=confidence,
                    match_notes=rec.get("match_notes", "")
                )
                db.add(m)

                evidence_list.append({
                    "source_type": rec["source_type"],
                    "match_tier": tier,
                    "confidence_score": confidence
                })

        score_data = score_case(evidence_list)
        score = models.Score(
            case_id=case_id,
            computed_score=score_data["computed_score"],
            confidence_tier=score_data["confidence_tier"],
            rationale=score_data["rationale"]
        )
        db.add(score)

        evidence_db = db.query(models.Match).filter_by(case_id=case_id).all()
        explain = build_explainability(score_data, evidence_db)
        conflicts = detect_conflicts(evidence_db)
        exp = models.Explainability(
            case_id=case_id,
            summary=explain["summary"],
            evidence_reasons=explain["evidence_reasons"],
            conflicts=conflicts
        )
        db.add(exp)

        case.status = "awaiting_review" if score_data["computed_score"] > 1 else "completed"
        db.commit()
    finally:
        db.close()

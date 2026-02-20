from sqlalchemy.orm import Session
from app import models

def create_case(db: Session, payload: dict):
    person = models.Person(
        full_name=payload["full_name"],
        dob=payload.get("dob"),
        address=payload.get("address"),
        email=payload.get("email"),
        phone=payload.get("phone"),
    )
    db.add(person)
    db.commit()
    db.refresh(person)

    consent = models.Consent(
        person_id=person.id,
        consent_text=payload["consent_text"],
    )
    db.add(consent)

    case = models.Case(person_id=person.id, status="created")
    db.add(case)
    db.commit()
    db.refresh(case)

    inputs = models.Input(case_id=case.id, input_json=payload)
    db.add(inputs)

    audit = models.AuditEvent(case_id=case.id, event_type="case_created")
    db.add(audit)

    db.commit()
    return case

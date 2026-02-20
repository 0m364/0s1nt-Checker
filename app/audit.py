from app import models
from datetime import datetime

def log_event(db, case_id: str, event_type: str, event_data: dict = None, user_id: str = None):
    event = models.AuditEvent(
        case_id=case_id,
        event_type=event_type,
        event_data=event_data or {},
        created_at=datetime.utcnow(),
    )
    if user_id:
        event.event_data["user_id"] = user_id
    db.add(event)
    db.commit()

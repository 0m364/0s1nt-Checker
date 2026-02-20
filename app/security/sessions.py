import secrets
from datetime import datetime, timedelta
from app import models

SESSION_TTL_HOURS = 8

def create_session(db, user_id):
    token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(hours=SESSION_TTL_HOURS)
    s = models.Session(user_id=user_id, token=token, expires_at=expires)
    db.add(s)
    db.commit()
    return token


def get_session(db, token):
    return db.query(models.Session).filter_by(token=token).first()

from fastapi import Request, HTTPException
from datetime import datetime
from app.security.sessions import get_session
from app.db import SessionLocal
from app import models


def get_current_user(request: Request):
    token = request.cookies.get("session")
    if not token:
        raise HTTPException(401, "Not authenticated")

    db = SessionLocal()
    s = get_session(db, token)
    if not s or s.expires_at < datetime.utcnow():
        raise HTTPException(401, "Session expired")

    user = db.query(models.User).get(s.user_id)
    return user

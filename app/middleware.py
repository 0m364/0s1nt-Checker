from starlette.middleware.base import BaseHTTPMiddleware
from app.db import SessionLocal
from app import models

class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        db = SessionLocal()
        try:
            user_id = getattr(request.state, "user_id", None)
            log = models.AccessLog(
                user_id=user_id,
                route=str(request.url.path),
                method=request.method,
                status_code=response.status_code
            )
            db.add(log)
            db.commit()
        finally:
            db.close()
        return response

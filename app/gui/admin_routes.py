from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.deps import get_db
from app import models
from app.security.deps import get_current_user
from app.security.rbac import require_role
from app.security.auth import hash_password

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/admin/users", response_class=HTMLResponse)
def list_users(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(user, ["admin"])
    users = db.query(models.User).order_by(models.User.created_at.desc()).all()
    return templates.TemplateResponse("admin_users.html", {"request": request, "users": users})

@router.post("/admin/users/create")
async def create_user(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(user, ["admin"])
    form = await request.form()
    new_user = models.User(
        username=form.get("username"),
        password_hash=hash_password(form.get("password")),
        role=form.get("role")
    )
    db.add(new_user)
    db.commit()
    return {"status": "created"}

@router.post("/admin/users/{user_id}/update")
async def update_user(user_id: str, request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(user, ["admin"])
    form = await request.form()
    u = db.query(models.User).get(user_id)
    if not u:
        raise HTTPException(404, "User not found")
    u.role = form.get("role", u.role)
    db.commit()
    return {"status": "updated"}

@router.post("/admin/users/{user_id}/reset-password")
async def reset_password(user_id: str, request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(user, ["admin"])
    form = await request.form()
    u = db.query(models.User).get(user_id)
    if not u:
        raise HTTPException(404, "User not found")
    u.password_hash = hash_password(form.get("new_password"))
    db.commit()
    return {"status": "password_reset"}

@router.get("/admin/analytics", response_class=HTMLResponse)
def analytics(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(user, ["admin"])
    total_cases = db.query(models.Case).count()
    by_status = db.query(models.Case.status, func.count()).group_by(models.Case.status).all()
    by_score = db.query(models.Score.computed_score, func.count()).group_by(models.Score.computed_score).all()
    by_source = db.query(models.Evidence.source_type, func.count()).group_by(models.Evidence.source_type).all()
    return templates.TemplateResponse("admin_analytics.html", {
        "request": request,
        "total_cases": total_cases,
        "by_status": by_status,
        "by_score": by_score,
        "by_source": by_source
    })

@router.get("/admin/data-quality", response_class=HTMLResponse)
def data_quality(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(user, ["admin"])
    total = db.query(models.Case).count()
    no_evidence = db.query(models.Case).filter(~models.Case.id.in_(db.query(models.Evidence.case_id))).count()
    low_conf = db.query(models.Match).filter(models.Match.match_tier.in_(["C","D"])).count()
    return templates.TemplateResponse("admin_data_quality.html", {
        "request": request,
        "total": total,
        "no_evidence": no_evidence,
        "low_conf": low_conf
    })

@router.get("/admin/audit", response_class=HTMLResponse)
def view_audit(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(user, ["admin"])
    logs = db.query(models.AccessLog).order_by(models.AccessLog.created_at.desc()).limit(500).all()
    return templates.TemplateResponse("audit.html", {"request": request, "logs": logs})

@router.get("/admin/audit/export/csv")
def export_access_logs_csv(db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(user, ["admin"])
    logs = db.query(models.AccessLog).order_by(models.AccessLog.created_at.desc()).all()
    def stream():
        yield "user_id,route,method,status_code,created_at\n"
        for l in logs:
            yield f"{l.user_id},{l.route},{l.method},{l.status_code},{l.created_at}\n"
    return StreamingResponse(stream(), media_type="text/csv")

@router.get("/admin/audit/export/json")
def export_access_logs_json(db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(user, ["admin"])
    logs = db.query(models.AccessLog).order_by(models.AccessLog.created_at.desc()).all()
    data = [
        {
            "user_id": str(l.user_id),
            "route": l.route,
            "method": l.method,
            "status_code": l.status_code,
            "created_at": str(l.created_at)
        }
        for l in logs
    ]
    return JSONResponse(data)

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.deps import get_db
from app import models

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/cases", response_class=HTMLResponse)
def list_cases(request: Request, db: Session = Depends(get_db)):
    cases = db.query(models.Case).order_by(models.Case.created_at.desc()).all()
    return templates.TemplateResponse("cases.html", {"request": request, "cases": cases})

@router.get("/cases/{case_id}", response_class=HTMLResponse)
def case_detail(case_id: str, request: Request, db: Session = Depends(get_db)):
    case = db.query(models.Case).get(case_id)
    person = db.query(models.Person).get(case.person_id)
    score = db.query(models.Score).filter_by(case_id=case_id).order_by(models.Score.created_at.desc()).first()

    evidence_rows = (
        db.query(models.Evidence, models.Match)
        .join(models.Match, models.Evidence.id == models.Match.evidence_id)
        .filter(models.Evidence.case_id == case_id)
        .all()
    )

    evidence = []
    for e, m in evidence_rows:
        evidence.append({
            "source_name": e.source_name,
            "source_type": e.source_type,
            "evidence_url": e.evidence_url,
            "record_id": e.record_id,
            "match_tier": m.match_tier,
            "confidence_score": float(m.confidence_score)
        })

    report = db.query(models.Report).filter_by(case_id=case_id).order_by(models.Report.generated_at.desc()).first()

    return templates.TemplateResponse("case_detail.html", {
        "request": request,
        "case": case,
        "person": person,
        "score": score,
        "evidence": evidence,
        "report": report
    })

@router.get("/cases/{case_id}/review", response_class=HTMLResponse)
def review_page(case_id: str, request: Request, db: Session = Depends(get_db)):
    case = db.query(models.Case).get(case_id)
    score = db.query(models.Score).filter_by(case_id=case_id).order_by(models.Score.created_at.desc()).first()

    evidence_rows = (
        db.query(models.Evidence, models.Match)
        .join(models.Match, models.Evidence.id == models.Match.evidence_id)
        .filter(models.Evidence.case_id == case_id)
        .all()
    )

    evidence = []
    for e, m in evidence_rows:
        evidence.append({
            "source_name": e.source_name,
            "source_type": e.source_type,
            "evidence_url": e.evidence_url,
            "record_id": e.record_id,
            "match_tier": m.match_tier,
            "confidence_score": float(m.confidence_score)
        })

    return templates.TemplateResponse("review.html", {
        "request": request,
        "case": case,
        "evidence": evidence,
        "score": score
    })

@router.get("/cases/{case_id}/timeline", response_class=HTMLResponse)
def case_timeline(case_id: str, request: Request, db: Session = Depends(get_db)):
    case = db.query(models.Case).get(case_id)
    events = (
        db.query(models.AuditEvent)
        .filter_by(case_id=case_id)
        .order_by(models.AuditEvent.created_at.asc())
        .all()
    )
    return templates.TemplateResponse("case_timeline.html", {"request": request, "case": case, "events": events})

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import os, tempfile
from app.deps import get_db
from app import schemas, crud, models
from app.pipeline.run_case import run_case_pipeline
from app.reports.pdf_builder import build_pdf
from app.reports.xlsx_builder import build_xlsx
from app.reports.context import build_report_context, build_xlsx_payload
from app.security.crypto import encrypt_file, decrypt_file
from app.audit import log_event

router = APIRouter()

@router.post("/cases")
def create_case(payload: schemas.CaseCreate, db: Session = Depends(get_db)):
    case = crud.create_case(db, payload.dict())
    log_event(db, str(case.id), "case_created", {"inputs": payload.dict()})
    return {"case_id": str(case.id), "status": case.status}

@router.post("/cases/{case_id}/run")
def run_case(case_id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    case = db.query(models.Case).get(case_id)
    if not case:
        raise HTTPException(404, "Case not found")
    case.status = "running"
    db.commit()
    log_event(db, case_id, "case_run_started")
    background_tasks.add_task(run_case_pipeline, None, case_id)
    return {"case_id": case_id, "status": "running"}

@router.get("/cases/{case_id}")
def get_case(case_id: str, db: Session = Depends(get_db)):
    case = db.query(models.Case).get(case_id)
    if not case:
        raise HTTPException(404, "Case not found")
    score = db.query(models.Score).filter_by(case_id=case_id).order_by(models.Score.created_at.desc()).first()
    return {
        "case_id": case_id,
        "status": case.status,
        "computed_score": score.computed_score if score else None,
        "confidence_tier": score.confidence_tier if score else None
    }

@router.post("/cases/{case_id}/review")
def review_case(case_id: str, payload: schemas.ReviewCreate, db: Session = Depends(get_db)):
    case = db.query(models.Case).get(case_id)
    if not case:
        raise HTTPException(404, "Case not found")

    review = models.Review(
        case_id=case_id,
        reviewer_name=payload.reviewer_name,
        decision=payload.decision,
        override_score=payload.override_score,
        notes=payload.notes
    )
    db.add(review)
    case.status = "completed" if payload.decision != "reject" else "rejected"
    db.commit()
    log_event(db, case_id, "case_reviewed", payload.dict())
    return {"case_id": case_id, "status": case.status}

@router.post("/cases/{case_id}/report")
def report_case(case_id: str, db: Session = Depends(get_db)):
    case = db.query(models.Case).get(case_id)
    if not case:
        raise HTTPException(404, "Case not found")
    person = db.query(models.Person).get(case.person_id)
    consent = db.query(models.Consent).filter_by(person_id=person.id).first()
    score = db.query(models.Score).filter_by(case_id=case_id).order_by(models.Score.created_at.desc()).first()
    evidence = db.query(models.Evidence).filter_by(case_id=case_id).all()
    reviews = db.query(models.Review).filter_by(case_id=case_id).all()

    context = build_report_context(case, person, consent, score, evidence, reviews)
    xlsx_payload = build_xlsx_payload(context)

    os.makedirs("reports", exist_ok=True)
    pdf_path = f"reports/{case_id}.pdf"
    xlsx_path = f"reports/{case_id}.xlsx"

    build_pdf(context, pdf_path)
    build_xlsx(xlsx_payload, xlsx_path)

    encrypt_file(pdf_path)
    encrypt_file(xlsx_path)

    report = models.Report(case_id=case_id, pdf_path=pdf_path + ".enc", xlsx_path=xlsx_path + ".enc")
    db.add(report)
    db.commit()
    log_event(db, case_id, "reports_generated")

    return {"pdf_path": report.pdf_path, "xlsx_path": report.xlsx_path}

@router.get("/cases/{case_id}/download/{fmt}")
def download_report(case_id: str, fmt: str, db: Session = Depends(get_db)):
    report = db.query(models.Report).filter_by(case_id=case_id).order_by(models.Report.generated_at.desc()).first()
    if not report:
        raise HTTPException(404, "No report found")

    enc_path = report.pdf_path if fmt == "pdf" else report.xlsx_path
    if not enc_path or not os.path.exists(enc_path):
        raise HTTPException(404, "File missing")

    tmp = tempfile.NamedTemporaryFile(delete=False)
    out_path = tmp.name
    decrypt_file(enc_path, out_path)
    return FileResponse(out_path, filename=f"{case_id}.{fmt}")

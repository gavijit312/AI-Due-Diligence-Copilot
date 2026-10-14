from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session
from api.deps import get_db
from core.models import AuditRun
from agents.graph import build_due_diligence_graph

router = APIRouter(prefix="/audit", tags=["Audit"])
graph_app = build_due_diligence_graph()


class AuditRequest(BaseModel):
    target_company: str = "Target Corporation"


def run_pipeline(audit_id: str, target_company: str, session_factory):
    db: Session = session_factory()
    audit_rec = db.query(AuditRun).filter(AuditRun.id == audit_id).first()
    if not audit_rec:
        db.close()
        return

    try:
        audit_rec.status = "RUNNING"
        db.commit()

        initial_state = {
            "session_id": str(audit_id),
            "uploaded_files": [],
            "target_company": target_company,
            "query": None,
            "legal_findings": None,
            "financial_findings": None,
            "compliance_findings": None,
            "risk_matrix": None,
            "executive_summary": None,
            "errors": []
        }

        final_state = graph_app.invoke(initial_state)

        audit_rec.status = "COMPLETED"
        audit_rec.risk_score = final_state.get("risk_matrix", {}).get("overall_risk_score", "MEDIUM")
        audit_rec.report = {
            "legal": final_state.get("legal_findings"),
            "financial": final_state.get("financial_findings"),
            "compliance": final_state.get("compliance_findings"),
            "risk_matrix": final_state.get("risk_matrix"),
            "executive_summary": final_state.get("executive_summary")
        }
        audit_rec.completed_at = datetime.utcnow()
        db.commit()
    except Exception as e:
        audit_rec.status = "FAILED"
        audit_rec.report = {"error": str(e)}
        db.commit()
    finally:
        db.close()


@router.post("/start")
def start_audit(payload: AuditRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    audit = AuditRun(target_company=payload.target_company, status="PENDING")
    db.add(audit)
    db.commit()
    db.refresh(audit)

    from core.database import SessionLocal
    background_tasks.add_task(run_pipeline, audit.id, payload.target_company, SessionLocal)

    return {"audit_id": str(audit.id), "status": "QUEUED"}


@router.get("/status/{audit_id}")
def check_status(audit_id: str, db: Session = Depends(get_db)):
    audit = db.query(AuditRun).filter(AuditRun.id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit run not found")
    return {
        "audit_id": str(audit.id),
        "status": audit.status,
        "risk_score": audit.risk_score,
        "report": audit.report
    }
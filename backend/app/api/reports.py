from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.compliance_report_service import (
    build_compliance_report,
    build_dashboard_kpis,
    build_pdf_report_structure,
    build_top_violations,
)

router = APIRouter(prefix="/reports", tags=["reports"], dependencies=[Depends(get_current_user)])


@router.get("/compliance")
def compliance_report(db: Session = Depends(get_db)) -> dict:
    return build_compliance_report(db)


@router.get("/compliance/kpis")
def compliance_dashboard_kpis(db: Session = Depends(get_db)) -> dict:
    return build_dashboard_kpis(db)


@router.get("/compliance/top-violations")
def compliance_top_violations(
    days: int = Query(default=7, ge=1, le=90),
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
) -> dict:
    return {
        "days": days,
        "items": build_top_violations(db, days=days, limit=limit),
    }


@router.get("/compliance/pdf-data")
def compliance_pdf_data(
    days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db),
) -> dict:
    return build_pdf_report_structure(db, days=days)

from app.api.deps import get_current_user
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.database.session import get_db
from app.models import User
from app.schemas.deployment import RuleTestRequest
from app.services.deployment_config_service import export_config_files, import_config_files
from app.services.deployment_diagnostics_service import build_diagnostics_report
from app.services.deployment_health_service import build_health_report
from app.services.deployment_setup_service import get_setup_status, test_compliance_rule, test_zone
from app.services.evidence_browser_service import browse_evidence
from app.services.runtime_metrics_service import runtime_metrics
from app.core.detectors import get_detector_registry

router = APIRouter(prefix="/deployment", tags=["deployment"], dependencies=[Depends(get_current_user)])


@router.get("/setup/status")
def setup_status(db: Session = Depends(get_db)) -> dict:
    return get_setup_status(db)


@router.get("/setup/verify")
def setup_verify(db: Session = Depends(get_db)) -> dict:
    return get_setup_status(db)


@router.get("/status")
def system_status(db: Session = Depends(get_db)) -> dict:
    health = build_health_report(db)
    metrics = runtime_metrics.refresh_runtime(db, detector_count=len(get_detector_registry().list()))
    camera = health["camera"]
    return {
        "overall": health["status"],
        "version": "2.0",
        "cameraOnline": camera["online"],
        "cameraOffline": camera["offline"],
        "cameraTotal": camera["total"],
        "rtspStatus": {
            "ffmpeg": health["ffmpeg"]["status"],
            "message": health["ffmpeg"].get("ffmpeg") or health["ffmpeg"].get("message"),
        },
        "storage": health["storage"],
        "cpu": build_diagnostics_report(db)["cpu"],
        "ram": build_diagnostics_report(db)["memory"],
        "gpu": build_diagnostics_report(db)["gpu"],
        "websocket": health["websocket"],
        "runtime": metrics,
    }


@router.get("/diagnostics")
def system_diagnostics(db: Session = Depends(get_db)) -> dict:
    return build_diagnostics_report(db)


@router.get("/zones/{zone_id}/test")
def zone_test_mode(zone_id: str, db: Session = Depends(get_db)) -> dict:
    try:
        return test_zone(db, zone_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/rules/test")
def rule_test_mode(payload: RuleTestRequest, db: Session = Depends(get_db)) -> dict:
    try:
        return test_compliance_rule(
            db,
            rule_type=payload.ruleType,
            track_id=payload.trackId,
            camera_id=payload.cameraId,
            zone_id=payload.zoneId,
            score_input=payload.score,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc


@router.get("/evidence")
def list_evidence(
    farmId: str | None = Query(default=None),
    cameraId: str | None = Query(default=None),
    date: str | None = Query(default=None, description="YYYY-MM-DD"),
    ruleType: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> dict:
    items, total = browse_evidence(
        db,
        farm_id=farmId,
        camera_id=cameraId,
        date_prefix=date,
        rule_type=ruleType,
        page=page,
        limit=limit,
    )
    return {"items": items, "total": total, "page": page, "limit": limit}


@router.get("/export")
def export_all_config(
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("backup.read")),
) -> dict:
    return export_config_files(db)


@router.get("/export/{config_name}")
def export_single_config(
    config_name: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("backup.read")),
) -> dict:
    bundle = export_config_files(db)
    key = f"{config_name}.json" if not config_name.endswith(".json") else config_name
    if key not in bundle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Config file not found")
    return {"file": key, "data": bundle[key], "meta": bundle.get("meta")}


@router.post("/import")
def import_all_config(
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("backup.write")),
) -> dict:
    from app.core.farm_access import is_super_admin

    if not is_super_admin(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ SUPER_ADMIN được import config")

    counts = import_config_files(db, payload)
    return {"status": "imported", "counts": counts}

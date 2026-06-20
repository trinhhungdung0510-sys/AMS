from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Camera
from app.schemas.zone_rule import ZoneRuleCreate, ZoneRuleResponse
from app.services.zone_rule_service import create_zone_rule, list_rules_for_camera, rule_to_response_dict

router = APIRouter(
    tags=["zone-rules"],
    dependencies=[Depends(get_current_user)],
)


def _to_response(rule) -> ZoneRuleResponse:
    return ZoneRuleResponse(**rule_to_response_dict(rule))


def _get_camera_or_404(camera_id: str, db: Session) -> Camera:
    camera = db.get(Camera, camera_id)
    if not camera:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy camera")
    return camera


@router.get("/cameras/{camera_id}/rules", response_model=list[ZoneRuleResponse])
def list_camera_rules(camera_id: str, db: Session = Depends(get_db)) -> list[ZoneRuleResponse]:
    _get_camera_or_404(camera_id, db)
    rules = list_rules_for_camera(db, camera_id)
    return [_to_response(rule) for rule in rules]


@router.post(
    "/cameras/{camera_id}/rules",
    response_model=ZoneRuleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_camera_rule(
    camera_id: str,
    payload: ZoneRuleCreate,
    db: Session = Depends(get_db),
) -> ZoneRuleResponse:
    try:
        rule = create_zone_rule(db, camera_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    return _to_response(rule)

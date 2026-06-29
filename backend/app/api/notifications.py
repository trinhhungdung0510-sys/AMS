from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.database.session import get_db
from app.models import NotificationDelivery, NotificationRule, User
from app.schemas.notification import NotificationRuleResponse
from app.schemas.violation_notification import (
    GmailConnectRequest,
    NotificationDeliveryResponse,
    NotificationSettingsResponse,
    NotificationSettingsUpdate,
    NotificationTestRequest,
    ZaloConnectPollResponse,
    ZaloConnectStartResponse,
)
from app.services.notification_connect_service import (
    NotificationConnectError,
    connect_gmail,
    poll_zalo_connect,
    start_zalo_connect,
)
from app.services.violation_notification_service import (
    build_test_api_response,
    get_notification_settings,
    mask_settings_for_api,
    run_dashboard_notification_test,
    run_gmail_notification_test,
    run_zalo_notification_test,
    save_notification_settings,
)

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
    dependencies=[Depends(get_current_user)],
)


def _connect_error(exc: NotificationConnectError) -> HTTPException:
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


@router.get("", response_model=list[NotificationRuleResponse])
def list_notification_rules(db: Session = Depends(get_db)) -> list[NotificationRule]:
    return list(db.scalars(select(NotificationRule).order_by(NotificationRule.id)))


@router.get("/settings", response_model=NotificationSettingsResponse)
def read_notification_settings(
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("settings.read")),
) -> NotificationSettingsResponse:
    return NotificationSettingsResponse(**mask_settings_for_api(get_notification_settings(db), db))


@router.put("/settings", response_model=NotificationSettingsResponse)
def update_notification_settings(
    payload: NotificationSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("settings.write")),
) -> NotificationSettingsResponse:
    updated = save_notification_settings(
        db,
        payload.model_dump(exclude_unset=True),
        updated_by=current_user.id,
    )
    return NotificationSettingsResponse(**mask_settings_for_api(updated, db))


@router.post("/connect/gmail", response_model=NotificationSettingsResponse)
def connect_gmail_channel(
    payload: GmailConnectRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("settings.write")),
) -> NotificationSettingsResponse:
    try:
        updated = connect_gmail(
            db,
            gmail_recipient=str(payload.gmail_recipient),
            updated_by=current_user.id,
        )
    except NotificationConnectError as exc:
        raise _connect_error(exc) from exc
    return NotificationSettingsResponse(**mask_settings_for_api(updated, db))


@router.post("/connect/zalo/start", response_model=ZaloConnectStartResponse)
def connect_zalo_start(
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("settings.write")),
) -> ZaloConnectStartResponse:
    try:
        payload = start_zalo_connect(db)
    except NotificationConnectError as exc:
        raise _connect_error(exc) from exc
    return ZaloConnectStartResponse(**payload)


@router.get("/connect/zalo/status/{session_id}", response_model=ZaloConnectPollResponse)
def connect_zalo_status(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("settings.write")),
) -> ZaloConnectPollResponse:
    try:
        result = poll_zalo_connect(db, session_id, updated_by=current_user.id)
    except NotificationConnectError as exc:
        raise _connect_error(exc) from exc

    settings = None
    if result.get("status") == "connected":
        settings = NotificationSettingsResponse(**mask_settings_for_api(result["settings"], db))
    return ZaloConnectPollResponse(
        status=result["status"],
        connected=result["connected"],
        settings=settings,
    )


@router.get("/deliveries", response_model=list[NotificationDeliveryResponse])
def list_notification_deliveries(
    event_id: str | None = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("settings.read")),
) -> list[NotificationDelivery]:
    query = select(NotificationDelivery).order_by(NotificationDelivery.sent_at.desc()).limit(min(limit, 200))
    if event_id:
        query = query.where(NotificationDelivery.event_id == event_id)
    return list(db.scalars(query))


@router.post("/test")
def send_test_notification(
    payload: NotificationTestRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("settings.write")),
) -> dict:
    farm_id = current_user.farm_id or "FARM-001"

    if payload.channel == "dashboard":
        result, _event, content = run_dashboard_notification_test(db, farm_id)
    elif payload.channel == "gmail":
        result, content = run_gmail_notification_test(db, farm_id)
    elif payload.channel == "zalo":
        result, content = run_zalo_notification_test(db, farm_id)
    else:
        result, _event, content = run_dashboard_notification_test(db, farm_id)

    response = build_test_api_response(result, content)
    if payload.channel == "dashboard" and result.status == "success":
        response["ephemeralEventId"] = content["event_id"]
        response["autoRemoveSeconds"] = 5
    return response

import uuid

from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.database.session import get_db
from app.models import User
from app.schemas.gmail_notification import (
    GmailConnectRequest,
    GmailConnectResponse,
    GmailTestResponse,
    GmailVerifyResponse,
    NotificationSendRequest,
    NotificationSendResponse,
)
from app.services.gmail_notification_service import (
    GmailNotificationError,
    connect_gmail_with_test_email,
    send_gmail_test,
    send_violation_gmail_for_event,
    verify_smtp_connection,
)
from app.services.violation_notification_service import (
    CHANNEL_GMAIL,
    NOTIFICATION_TITLE,
    _record_delivery,
    get_notification_settings,
)

router = APIRouter(
    prefix="/notification",
    tags=["notification"],
    dependencies=[Depends(get_current_user)],
)


def _gmail_error(exc: GmailNotificationError) -> HTTPException:
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


@router.post("/gmail/connect", response_model=GmailConnectResponse)
def gmail_connect(
    payload: GmailConnectRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("settings.write")),
) -> GmailConnectResponse:
    try:
        updated = connect_gmail_with_test_email(
            db,
            gmail_recipient=str(payload.gmail_recipient),
            updated_by=current_user.id,
        )
    except GmailNotificationError as exc:
        raise _gmail_error(exc) from exc

    return GmailConnectResponse(
        connected=True,
        gmail_recipient=updated.get("gmail_recipient") or str(payload.gmail_recipient),
    )


@router.post("/gmail/verify", response_model=GmailVerifyResponse)
def gmail_verify(
    _: User = Depends(require_permission("settings.write")),
) -> GmailVerifyResponse:
    try:
        verify_smtp_connection()
    except GmailNotificationError as exc:
        raise _gmail_error(exc) from exc
    return GmailVerifyResponse()


@router.post("/gmail/test", response_model=GmailTestResponse)
def gmail_test(
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("settings.write")),
) -> GmailTestResponse:
    try:
        result = send_gmail_test(db)
    except GmailNotificationError as exc:
        raise _gmail_error(exc) from exc

    event_id = f"TST-GML-{uuid.uuid4().hex[:6].upper()}"
    _record_delivery(
        db,
        event_id=event_id,
        farm_id="FARM-001",
        channel=CHANNEL_GMAIL,
        status="success" if result.success else "failed",
        subject=NOTIFICATION_TITLE,
        error_message=result.error,
        recipient=result.recipient,
        smtp_latency_ms=result.smtp_latency_ms,
    )
    db.commit()

    if not result.success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.error or "Gửi thất bại")

    return GmailTestResponse(success=True, recipient=result.recipient, error=None)


@router.post("/send", response_model=NotificationSendResponse)
def notification_send(
    payload: NotificationSendRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("settings.write")),
) -> NotificationSendResponse:
    event = payload.model_dump()
    event["metadata"] = event.get("metadata") or {"source": "compliance_engine"}
    result = send_violation_gmail_for_event(db, event)
    settings = get_notification_settings(db)
    recipient = settings.get("gmail_recipient")

    _record_delivery(
        db,
        event_id=payload.event_id,
        farm_id=payload.farm_id,
        channel=CHANNEL_GMAIL,
        status=result.status,
        subject=NOTIFICATION_TITLE,
        error_message=result.error,
        recipient=recipient,
        smtp_latency_ms=result.smtp_latency_ms,
    )
    db.commit()

    if result.status != "success":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.error or "Gửi thất bại")

    return NotificationSendResponse(
        status=result.status,
        error=result.error,
        recipient=recipient,
    )

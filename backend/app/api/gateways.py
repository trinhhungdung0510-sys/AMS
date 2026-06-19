from app.api.deps import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import NotificationGateway
from app.schemas.gateway import NotificationGatewayResponse

router = APIRouter(prefix="/notification-gateways", tags=["notification-gateways"],
    dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=list[NotificationGatewayResponse])
def list_notification_gateways(db: Session = Depends(get_db)) -> list[NotificationGateway]:
    return list(db.scalars(select(NotificationGateway).order_by(NotificationGateway.id)))

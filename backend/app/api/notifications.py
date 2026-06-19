from app.api.deps import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import NotificationRule
from app.schemas.notification import NotificationRuleResponse

router = APIRouter(prefix="/notifications", tags=["notifications"],
    dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=list[NotificationRuleResponse])
def list_notification_rules(db: Session = Depends(get_db)) -> list[NotificationRule]:
    return list(db.scalars(select(NotificationRule).order_by(NotificationRule.id)))

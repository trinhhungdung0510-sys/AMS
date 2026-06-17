from pydantic import BaseModel, ConfigDict


class NotificationRuleResponse(BaseModel):
    id: str
    name: str
    alert_category: str
    severity: str
    email: bool
    telegram: bool
    zalo: bool
    enabled: bool

    model_config = ConfigDict(from_attributes=True)

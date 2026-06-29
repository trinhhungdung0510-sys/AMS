from pydantic import BaseModel, EmailStr, Field


class GmailConnectRequest(BaseModel):
    gmail_recipient: EmailStr


class GmailConnectResponse(BaseModel):
    connected: bool = True
    gmail_recipient: str = ""


class GmailVerifyResponse(BaseModel):
    ok: bool = True
    message: str = "Kết nối SMTP Gmail thành công"


class GmailTestResponse(BaseModel):
    success: bool
    recipient: str
    error: str | None = None


class NotificationSendRequest(BaseModel):
    event_id: str = Field(min_length=1, max_length=20)
    farm_id: str = "FARM-001"
    status: str = "OPEN"
    category: str = "compliance_violation"
    event_type: str = "NO_HAND_SANITIZE"
    severity: str = "HIGH"
    severityLabel: str | None = None
    camera_id: str | None = None
    camera_name: str | None = None
    zone_name: str | None = None
    rule_name: str | None = None
    description: str | None = None
    started_at: str | None = None
    snapshot_url: str | None = None
    metadata: dict | None = None


class NotificationSendResponse(BaseModel):
    channel: str = "gmail"
    status: str
    error: str | None = None
    recipient: str | None = None

from pydantic import BaseModel, EmailStr, Field


class NotificationSettingsResponse(BaseModel):
    gmail_enabled: bool = True
    gmail_recipient: str = ""
    gmail_connected: bool = False
    gmail_last_sent_at: str | None = None
    gmail_last_status: str | None = None
    gmail_last_error: str | None = None
    zalo_enabled: bool = True
    zalo_connected: bool = False
    ams_app_url: str = ""


class NotificationSettingsUpdate(BaseModel):
    gmail_enabled: bool | None = None
    zalo_enabled: bool | None = None
    gmail_recipient: str | None = None
    ams_app_url: str | None = None


class GmailConnectRequest(BaseModel):
    gmail_recipient: EmailStr


class ZaloConnectStartResponse(BaseModel):
    session_id: str
    follow_url: str
    qr_url: str
    expires_in: int
    message: str


class ZaloConnectPollResponse(BaseModel):
    status: str
    connected: bool
    settings: NotificationSettingsResponse | None = None


class NotificationDeliveryResponse(BaseModel):
    id: str
    event_id: str
    farm_id: str
    channel: str
    status: str
    sent_at: str
    subject: str | None = None
    recipient: str | None = None
    smtp_latency_ms: int | None = None
    error_message: str | None = None


class NotificationTestRequest(BaseModel):
    channel: str = Field(default="dashboard", pattern="^(dashboard|gmail|zalo)$")

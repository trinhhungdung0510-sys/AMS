from pydantic import BaseModel, ConfigDict


class NotificationGatewayResponse(BaseModel):
    id: str
    farm_id: str
    gateway_type: str
    endpoint: str
    enabled: bool
    status: str

    model_config = ConfigDict(from_attributes=True)

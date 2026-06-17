from pydantic import BaseModel, ConfigDict


class CameraResponse(BaseModel):
    id: str
    farm_id: str
    name: str
    zone: str
    ip_address: str
    status: str
    resolution: str
    uptime: float
    fps: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

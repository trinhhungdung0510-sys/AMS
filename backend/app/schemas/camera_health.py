from pydantic import BaseModel, ConfigDict


class CameraHealthResponse(BaseModel):
    id: str
    farm_id: str
    camera_id: str
    fps: int
    bitrate: float
    last_seen: str
    status: str

    model_config = ConfigDict(from_attributes=True)

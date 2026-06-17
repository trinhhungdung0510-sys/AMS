from pydantic import BaseModel, ConfigDict


class CameraStreamResponse(BaseModel):
    id: str
    camera_id: str
    rtsp_url: str
    fps: int
    resolution: str
    stream_status: str

    model_config = ConfigDict(from_attributes=True)

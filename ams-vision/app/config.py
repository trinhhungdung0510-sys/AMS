from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class VisionSettings(BaseSettings):
    service_name: str = "AMS Vision"
    backend_base_url: str = "http://127.0.0.1:8000"
    camera_id: str = "CAM-001"
    rtsp_url: str = "rtsp://example.local/live"
    mock_detection: bool = True
    mock_detection_interval: int = 30
    snapshots_dir: str = "/app/snapshots"
    track_history_path: str = "/app/snapshots/tracks_history.json"
    yolo_model: str = "yolov8n.pt"
    publish_category: str = "restricted_zone_intrusion"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> VisionSettings:
    return VisionSettings()

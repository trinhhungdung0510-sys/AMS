from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AMS Backend"
    api_prefix: str = "/api"
    environment: str = "development"
    database_url: str = "postgresql+psycopg://ams:ams_password@localhost:5432/ams"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret_key: str = "ams-dev-secret-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    cors_origins: str = (
        "http://localhost:5173,http://localhost:5174,https://ams-rust-gamma.vercel.app"
    )
    employee_storage_dir: str = "storage/employees"
    storage_root: str = "storage"
    ffprobe_path: str = "ffprobe"
    ffmpeg_path: str = "ffmpeg"
    camera_rtsp_test_timeout_seconds: int = 15
    camera_snapshot_timeout_seconds: int = 20
    uploads_root: str = "uploads"
    yolo_model_path: str = "yolov8n.pt"
    yolo_confidence: float = 0.5
    yolo_fps_limit: float = 5.0
    yolo_prefer_bytetrack: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

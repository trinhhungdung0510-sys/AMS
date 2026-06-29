import logging
import os
from functools import lru_cache
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


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
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,https://ams-rust-gamma.vercel.app"
    )
    employee_storage_dir: str = "storage/employees"
    storage_root: str = "storage"
    ffprobe_path: str = "ffprobe"
    ffmpeg_path: str = "ffmpeg"
    camera_rtsp_test_timeout_seconds: int = 15
    camera_snapshot_timeout_seconds: int = 20
    uploads_root: str = "uploads"
    compliance_uniform_threshold: float = 0.85
    compliance_save_evidence: bool = True
    compliance_evidence_subdir: str = "evidence"
    demo_mode: bool = False
    demo_auto_start: bool = True
    demo_seed_on_startup: bool = True
    demo_seed_count: int = 12
    demo_interval_seconds: int = 20
    demo_assets_dir: str = "demo-assets"
    workflow_timeout_seconds: int = 300
    retention_days: int = 90
    stress_test_enabled: bool = False
    yolo_model_path: str = "yolov8n.pt"
    yolo_confidence: float = 0.5
    yolo_fps_limit: float = 5.0
    yolo_prefer_bytetrack: bool = True
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    zalo_oa_access_token: str = ""
    zalo_oa_id: str = ""
    zalo_oa_follow_url: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
    )

    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


def log_smtp_config_presence(*, source: str = "resolve_smtp_credentials") -> None:
    """Debug SMTP presence without logging secrets."""
    creds = resolve_smtp_credentials()
    logger.info(
        "[%s] SMTP_USER exists=%s SMTP_PASSWORD exists=%s",
        source,
        bool((creds.get("user") or "").strip()),
        bool(creds.get("password") or ""),
    )


def resolve_smtp_credentials() -> dict[str, Any]:
    """
    Read SMTP from the current process environment first (Docker env_file / compose),
    then fall back to Settings (.env via pydantic). Avoids stale @lru_cache for secrets
    when only os.environ was updated at container start.
    """
    settings = get_settings()

    user = (os.environ.get("SMTP_USER") or settings.smtp_user or "").strip()
    password = os.environ.get("SMTP_PASSWORD") or settings.smtp_password or ""
    host = (os.environ.get("SMTP_HOST") or settings.smtp_host or "").strip()
    port_raw = os.environ.get("SMTP_PORT") or settings.smtp_port or 587

    try:
        port = int(port_raw)
    except (TypeError, ValueError):
        port = 587

    return {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "sender": user,
    }

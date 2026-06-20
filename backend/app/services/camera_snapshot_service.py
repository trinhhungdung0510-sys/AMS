from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from app.core.config import get_settings
from app.models import Camera
from app.services.camera_registry import build_rtsp_url
from app.services.ffmpeg_utils import normalize_ffmpeg_error


@dataclass
class CameraSnapshotResult:
    success: bool
    url: str | None = None
    error: str | None = None
    captured_at: str | None = None
    file_path: Path | None = None


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def snapshot_storage_dir(camera_id: str) -> Path:
    settings = get_settings()
    directory = Path(settings.uploads_root) / "snapshots" / camera_id
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def build_snapshot_filename(captured_at: datetime | None = None) -> str:
    moment = captured_at or datetime.now(timezone.utc)
    return f"snapshot_{moment.strftime('%Y%m%d_%H%M%S')}.jpg"


def build_snapshot_public_url(camera_id: str, filename: str) -> str:
    return f"/uploads/snapshots/{camera_id}/{filename}"


def resolve_camera_rtsp_url(camera: Camera) -> str | None:
    if camera.rtsp_url and camera.rtsp_url.strip():
        return camera.rtsp_url.strip()
    if not camera.ip or not camera.username:
        return None
    return build_rtsp_url(
        ip=camera.ip,
        port=camera.port,
        username=camera.username,
        password=camera.password,
        rtsp_url=camera.rtsp_url,
    )


def _validate_camera_for_capture(camera: Camera) -> CameraSnapshotResult | None:
    if camera.status.lower() != "online":
        return CameraSnapshotResult(success=False, error="Camera đang offline")
    if not camera.is_active:
        return CameraSnapshotResult(success=False, error="Camera chưa được kích hoạt")

    rtsp_url = resolve_camera_rtsp_url(camera)
    if not rtsp_url:
        return CameraSnapshotResult(success=False, error="Camera chưa có URL RTSP hợp lệ")
    if not rtsp_url.lower().startswith("rtsp://"):
        return CameraSnapshotResult(success=False, error="URL RTSP không hợp lệ")
    return None


def capture_snapshot_from_rtsp(
    *,
    camera_id: str,
    rtsp_url: str,
    captured_at: datetime | None = None,
) -> CameraSnapshotResult:
    settings = get_settings()
    ffmpeg_bin = settings.ffmpeg_path
    timeout_seconds = settings.camera_snapshot_timeout_seconds

    if not shutil.which(ffmpeg_bin):
        return CameraSnapshotResult(
            success=False,
            error="ffmpeg chưa được cài trên server — cài FFmpeg (brew install ffmpeg / apt install ffmpeg)",
        )

    moment = captured_at or datetime.now(timezone.utc)
    filename = build_snapshot_filename(moment)
    output_path = snapshot_storage_dir(camera_id) / filename

    command = [
        ffmpeg_bin,
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-rtsp_transport",
        "tcp",
        "-timeout",
        str(timeout_seconds * 1_000_000),
        "-i",
        rtsp_url,
        "-frames:v",
        "1",
        "-q:v",
        "2",
        str(output_path),
    ]

    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_seconds + 5,
            check=False,
        )
    except subprocess.TimeoutExpired:
        if output_path.exists():
            output_path.unlink(missing_ok=True)
        return CameraSnapshotResult(
            success=False,
            error=f"Hết thời gian chờ sau {timeout_seconds} giây",
        )

    if completed.returncode != 0 or not output_path.exists() or output_path.stat().st_size == 0:
        output_path.unlink(missing_ok=True)
        return CameraSnapshotResult(
            success=False,
            error=normalize_ffmpeg_error(completed.stderr, completed.returncode),
        )

    captured_iso = moment.isoformat()
    return CameraSnapshotResult(
        success=True,
        url=build_snapshot_public_url(camera_id, filename),
        captured_at=captured_iso,
        file_path=output_path,
    )


def capture_camera_snapshot(camera: Camera) -> CameraSnapshotResult:
    validation_error = _validate_camera_for_capture(camera)
    if validation_error:
        return validation_error

    rtsp_url = resolve_camera_rtsp_url(camera)
    if not rtsp_url:
        return CameraSnapshotResult(success=False, error="Camera chưa có URL RTSP hợp lệ")

    return capture_snapshot_from_rtsp(camera_id=camera.id, rtsp_url=rtsp_url)


def get_latest_camera_snapshot(camera_id: str) -> CameraSnapshotResult:
    directory = snapshot_storage_dir(camera_id)
    files = sorted(
        directory.glob("snapshot_*.jpg"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not files:
        return CameraSnapshotResult(success=False, error="Chưa có snapshot nào cho camera này")

    latest = files[0]
    captured_at = datetime.fromtimestamp(latest.stat().st_mtime, tz=timezone.utc).isoformat()
    return CameraSnapshotResult(
        success=True,
        url=build_snapshot_public_url(camera_id, latest.name),
        captured_at=captured_at,
        file_path=latest,
    )


def snapshot_result_to_dict(result: CameraSnapshotResult) -> dict:
    return {
        "success": result.success,
        "url": result.url,
        "error": result.error,
        "captured_at": result.captured_at,
    }

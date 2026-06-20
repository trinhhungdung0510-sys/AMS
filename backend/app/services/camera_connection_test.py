from __future__ import annotations

import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from fractions import Fraction

from app.core.config import get_settings
from app.services.ffmpeg_utils import normalize_ffmpeg_error


@dataclass
class CameraConnectionProbeResult:
    success: bool
    fps: int | None = None
    resolution: str | None = None
    error: str | None = None


def _parse_fps(value: str | None) -> int | None:
    if not value or value in {"0/0", "N/A"}:
        return None
    try:
        fps = float(Fraction(value))
    except (ValueError, ZeroDivisionError):
        return None
    if fps <= 0:
        return None
    return round(fps)


def probe_rtsp_stream(rtsp_url: str) -> CameraConnectionProbeResult:
    settings = get_settings()
    ffprobe_bin = settings.ffprobe_path
    timeout_seconds = settings.camera_rtsp_test_timeout_seconds

    cleaned_url = rtsp_url.strip()
    if not cleaned_url.lower().startswith("rtsp://"):
        return CameraConnectionProbeResult(success=False, error="URL RTSP phải bắt đầu bằng rtsp://")

    if not shutil.which(ffprobe_bin):
        return CameraConnectionProbeResult(
            success=False,
            error="ffprobe chưa được cài trên server — cài FFmpeg (brew install ffmpeg / apt install ffmpeg)",
        )

    command = [
        ffprobe_bin,
        "-hide_banner",
        "-loglevel",
        "error",
        "-rtsp_transport",
        "tcp",
        "-timeout",
        str(timeout_seconds * 1_000_000),
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height,avg_frame_rate,r_frame_rate",
        "-of",
        "json",
        cleaned_url,
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
        return CameraConnectionProbeResult(
            success=False,
            error=f"Hết thời gian chờ sau {timeout_seconds} giây",
        )

    if completed.returncode != 0:
        return CameraConnectionProbeResult(
            success=False,
            error=normalize_ffmpeg_error(completed.stderr, completed.returncode),
        )

    try:
        payload = json.loads(completed.stdout or "{}")
    except json.JSONDecodeError:
        return CameraConnectionProbeResult(success=False, error="Không đọc được phản hồi từ ffprobe")

    streams = payload.get("streams") or []
    if not streams:
        return CameraConnectionProbeResult(success=False, error="Không tìm thấy luồng video trên RTSP URL")

    stream = streams[0]
    width = stream.get("width")
    height = stream.get("height")
    if not width or not height:
        return CameraConnectionProbeResult(success=False, error="Không lấy được độ phân giải từ stream")

    fps = _parse_fps(stream.get("avg_frame_rate")) or _parse_fps(stream.get("r_frame_rate"))
    if fps is None:
        fps_match = re.search(r"(\d+(?:\.\d+)?)\s*fps", completed.stderr, re.IGNORECASE)
        if fps_match:
            fps = round(float(fps_match.group(1)))

    return CameraConnectionProbeResult(
        success=True,
        fps=fps or 25,
        resolution=f"{width}x{height}",
    )

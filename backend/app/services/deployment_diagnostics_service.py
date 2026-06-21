from __future__ import annotations

import os
import platform
import shutil
import socket
import subprocess
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Camera
from app.services.camera_connection_test import probe_rtsp_stream


def _disk_diagnostics() -> dict[str, Any]:
    usage = shutil.disk_usage("/")
    return {
        "totalGb": round(usage.total / (1024**3), 2),
        "usedGb": round(usage.used / (1024**3), 2),
        "freeGb": round(usage.free / (1024**3), 2),
        "percentUsed": round((usage.used / usage.total) * 100, 1) if usage.total else 0,
    }


def _memory_diagnostics() -> dict[str, Any]:
    try:
        page_size = os.sysconf("SC_PAGE_SIZE")
        total_pages = os.sysconf("SC_PHYS_PAGES")
        avail_pages = os.sysconf("SC_AVAILPHYS")
        total = page_size * total_pages
        available = page_size * avail_pages
        used = total - available
        return {
            "totalGb": round(total / (1024**3), 2),
            "usedGb": round(used / (1024**3), 2),
            "availableGb": round(available / (1024**3), 2),
            "percentUsed": round((used / total) * 100, 1) if total else 0,
        }
    except (AttributeError, ValueError, OSError):
        return {"status": "unknown"}


def _cpu_diagnostics() -> dict[str, Any]:
    info = {
        "cores": os.cpu_count() or 0,
        "platform": platform.processor() or platform.machine(),
    }
    try:
        load1, load5, load15 = os.getloadavg()
        info.update({"load1": round(load1, 2), "load5": round(load5, 2), "load15": round(load15, 2)})
    except (AttributeError, OSError):
        pass
    return info


def _gpu_diagnostics() -> dict[str, Any]:
    nvidia_smi = shutil.which("nvidia-smi")
    if not nvidia_smi:
        return {"status": "not_detected", "message": "No NVIDIA GPU tooling found"}
    try:
        result = subprocess.run(
            [nvidia_smi, "--query-gpu=name,memory.used,memory.total,utilization.gpu", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if result.returncode != 0:
            return {"status": "error", "message": result.stderr.strip() or "nvidia-smi failed"}
        lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        return {"status": "ok", "devices": lines}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


def _network_diagnostics() -> dict[str, Any]:
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        local_ip = "unknown"
    return {"hostname": hostname, "localIp": local_ip}


def _camera_reachability(db: Session, limit: int = 10) -> list[dict[str, Any]]:
    cameras = list(db.scalars(select(Camera).where(Camera.is_active.is_(True)).limit(limit)))
    results = []
    for camera in cameras:
        rtsp_url = getattr(camera, "rtsp_url", None) or ""
        if not rtsp_url:
            results.append(
                {
                    "cameraId": camera.id,
                    "cameraName": camera.name,
                    "reachable": None,
                    "status": "no_rtsp_url",
                    "message": "RTSP URL not configured",
                }
            )
            continue
        probe = probe_rtsp_stream(rtsp_url)
        results.append(
            {
                "cameraId": camera.id,
                "cameraName": camera.name,
                "reachable": probe.success,
                "status": "online" if probe.success else "offline",
                "fps": probe.fps,
                "resolution": probe.resolution,
                "message": probe.error,
            }
        )
    return results


def build_diagnostics_report(db: Session) -> dict[str, Any]:
    return {
        "disk": _disk_diagnostics(),
        "memory": _memory_diagnostics(),
        "cpu": _cpu_diagnostics(),
        "gpu": _gpu_diagnostics(),
        "network": _network_diagnostics(),
        "cameraReachability": _camera_reachability(db),
    }

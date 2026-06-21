from __future__ import annotations

import re
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw

from app.compliance.config import get_compliance_settings
from app.core.config import get_settings


def _sanitize_timestamp(timestamp: str) -> str:
    cleaned = re.sub(r"[^0-9T\-:+Z]", "", timestamp or "")
    return cleaned.replace(":", "-") or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")


def save_evidence_snapshot(
    *,
    timestamp: str,
    bbox: list[float] | tuple[float, float, float, float] | None = None,
    label: str = "Person",
) -> str | None:
    """
    Save JPEG evidence to uploads/evidence/YYYY/MM/DD/event_<timestamp>.jpg

    Returns public URL path (/uploads/...) or None when save_evidence is disabled.
    Skips write when file already exists.
    """
    settings = get_compliance_settings()
    if not settings.save_evidence:
        return None

    app_settings = get_settings()
    now = datetime.now(timezone.utc)
    date_parts = now.strftime("%Y/%m/%d")
    safe_ts = _sanitize_timestamp(timestamp)
    filename = f"event_{safe_ts}.jpg"
    relative_dir = Path(settings.evidence_subdir) / date_parts
    storage_dir = Path(app_settings.uploads_root) / relative_dir
    storage_dir.mkdir(parents=True, exist_ok=True)
    destination = storage_dir / filename

    public_path = f"/uploads/{relative_dir.as_posix()}/{filename}"
    if destination.exists():
        return public_path

    image = _render_evidence_image(bbox=bbox, label=label, timestamp=timestamp or now.isoformat())
    image.save(destination, format="JPEG", quality=92, optimize=True)
    return public_path


def _render_evidence_image(
    *,
    bbox: list[float] | tuple[float, float, float, float] | None,
    label: str,
    timestamp: str,
) -> Image.Image:
    width, height = 1280, 720
    image = Image.new("RGB", (width, height), color=(24, 28, 36))
    draw = ImageDraw.Draw(image)

    if bbox and len(bbox) == 4:
        x1, y1, x2, y2 = bbox
        if max(bbox) <= 1.0:
            x1, x2 = x1 * width, x2 * width
            y1, y2 = y1 * height, y2 * height
        draw.rectangle([x1, y1, x2, y2], outline=(239, 68, 68), width=4)

    draw.rectangle([0, 0, width, 48], fill=(15, 23, 42))
    draw.text((16, 14), f"AMS Evidence — {label}", fill=(248, 250, 252))
    draw.text((16, height - 32), timestamp, fill=(203, 213, 225))
    return image

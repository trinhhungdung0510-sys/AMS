from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import EventSnapshot

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
THUMB_WIDTH = 320

SEVERITY_COLORS = {
    "critical": (220, 38, 38),
    "high": (234, 88, 12),
    "warning": (202, 138, 4),
    "danger": (220, 38, 38),
    "info": (37, 99, 235),
}


@dataclass
class SnapshotAnnotation:
    object_label: str
    zone_name: str
    rule_name: str
    timestamp: str
    severity: str
    bbox: Optional[tuple[int, int, int, int]] = None
    track_id: Optional[int] = None
    confidence: Optional[float] = None


from app.services.vi_localization import resolve_zone_name as resolve_zone_display_name


def create_event_snapshot(
    *,
    event_id: str,
    snapshot_id: str,
    storage_category: str,
    annotation: SnapshotAnnotation,
) -> EventSnapshot:
    image_path, thumbnail_path = generate_snapshot_files(
        event_id=event_id,
        storage_category=storage_category,
        annotation=annotation,
    )
    return EventSnapshot(
        id=snapshot_id,
        event_id=event_id,
        image_path=image_path,
        thumbnail_path=thumbnail_path,
    )


def generate_snapshot_files(
    *,
    event_id: str,
    storage_category: str,
    annotation: SnapshotAnnotation,
) -> tuple[str, str]:
    settings = get_settings()
    category_dir = Path(settings.storage_root) / storage_category
    thumb_dir = category_dir / "thumbs"
    category_dir.mkdir(parents=True, exist_ok=True)
    thumb_dir.mkdir(parents=True, exist_ok=True)

    image = render_annotated_snapshot(annotation)
    image_path = category_dir / f"{event_id}.jpg"
    thumb_path = thumb_dir / f"{event_id}.jpg"
    image.save(image_path, format="JPEG", quality=92, optimize=True)
    image.resize(
        (_scaled_width(image.width, THUMB_WIDTH), _scaled_height(image.width, image.height, THUMB_WIDTH)),
        Image.Resampling.LANCZOS,
    ).save(thumb_path, format="JPEG", quality=85, optimize=True)

    return (
        f"/storage/{storage_category}/{event_id}.jpg",
        f"/storage/{storage_category}/thumbs/{event_id}.jpg",
    )


def render_annotated_snapshot(annotation: SnapshotAnnotation) -> Image.Image:
    image = _create_base_frame()
    draw = ImageDraw.Draw(image)
    title_font = _load_font(28)
    label_font = _load_font(22)
    meta_font = _load_font(20)
    small_font = _load_font(18)

    bbox = annotation.bbox or _default_bbox(annotation.track_id)
    color = SEVERITY_COLORS.get(annotation.severity.lower(), (37, 99, 235))

    x1, y1, x2, y2 = bbox
    draw.rectangle((x1, y1, x2, y2), outline=color, width=4)
    draw.rectangle((x1 + 2, y1 + 2, x2 - 2, y2 - 2), outline=(255, 255, 255), width=1)

    object_text = annotation.object_label
    if annotation.track_id is not None:
        object_text = f"{object_text} #{annotation.track_id}"
    if annotation.confidence is not None:
        object_text = f"{object_text} ({annotation.confidence:.0f}%)"

    tag_height = 30
    tag_width = min(FRAME_WIDTH - x1 - 8, max(180, len(object_text) * 11 + 20))
    draw.rectangle((x1, max(0, y1 - tag_height - 4), x1 + tag_width, max(0, y1 - 4)), fill=color)
    draw.text((x1 + 10, max(4, y1 - tag_height)), object_text, fill=(255, 255, 255), font=label_font)

    panel_top = FRAME_HEIGHT - 150
    draw.rectangle((0, panel_top, FRAME_WIDTH, FRAME_HEIGHT), fill=(15, 23, 42))
    draw.rectangle((0, panel_top, FRAME_WIDTH, panel_top + 4), fill=color)

    lines = [
        ("Zone", annotation.zone_name),
        ("Rule", annotation.rule_name),
        ("Time", _format_timestamp(annotation.timestamp)),
        ("Severity", annotation.severity.upper()),
    ]
    y = panel_top + 16
    for label, value in lines:
        draw.text((24, y), f"{label}:", fill=(148, 163, 184), font=small_font)
        value_color = color if label == "Severity" else (248, 250, 252)
        draw.text((120, y), value[:72], fill=value_color, font=meta_font)
        y += 30

    draw.text((FRAME_WIDTH - 210, 18), "AMS Snapshot v3.5", fill=(148, 163, 184), font=title_font)
    return image


def render_annotated_snapshot_bytes(annotation: SnapshotAnnotation) -> bytes:
    buffer = BytesIO()
    render_annotated_snapshot(annotation).save(buffer, format="JPEG", quality=92, optimize=True)
    return buffer.getvalue()


def _create_base_frame() -> Image.Image:
    image = Image.new("RGB", (FRAME_WIDTH, FRAME_HEIGHT), (28, 72, 38))
    draw = ImageDraw.Draw(image)
    for x in range(0, FRAME_WIDTH, 80):
        draw.line((x, 0, x, FRAME_HEIGHT), fill=(34, 84, 48), width=1)
    for y in range(0, FRAME_HEIGHT, 80):
        draw.line((0, y, FRAME_WIDTH, y), fill=(34, 84, 48), width=1)
    draw.text((48, 48), "Camera Feed", fill=(187, 247, 208), font=_load_font(24))
    return image


def _default_bbox(track_id: Optional[int]) -> tuple[int, int, int, int]:
    seed = track_id or 1
    x1 = 420 + (seed * 37) % 260
    y1 = 160 + (seed * 53) % 180
    return (x1, y1, x1 + 280, y1 + 360)


def _format_timestamp(timestamp: str) -> str:
    normalized = timestamp.replace("T", " ").replace("+07:00", " +07").replace("Z", " UTC")
    return normalized[:32]


def _scaled_width(width: int, target_width: int) -> int:
    return target_width


def _scaled_height(width: int, height: int, target_width: int) -> int:
    return max(1, int(height * (target_width / width)))


def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "arial.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()

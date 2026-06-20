from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AiDetection, Camera
from app.schemas.ai_detection import AiDetectionCreate


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_detection_id() -> str:
    return f"AID-{uuid.uuid4().hex[:10].upper()}"


def detection_to_response_dict(detection: AiDetection) -> dict:
    return {
        "id": detection.id,
        "camera_id": detection.camera_id,
        "label": detection.label,
        "confidence": detection.confidence,
        "bbox": detection.bbox,
        "created_at": detection.created_at,
    }


def _bbox_payload(bbox) -> dict:
    return {
        "x": float(bbox.x),
        "y": float(bbox.y),
        "w": float(bbox.w),
        "h": float(bbox.h),
    }


def list_detections_for_camera(db: Session, camera_id: str) -> list[AiDetection]:
    return list(
        db.scalars(
            select(AiDetection)
            .where(AiDetection.camera_id == camera_id)
            .order_by(AiDetection.created_at.desc(), AiDetection.id)
        )
    )


def create_detection(db: Session, camera_id: str, payload: AiDetectionCreate) -> AiDetection:
    camera = db.get(Camera, camera_id)
    if not camera:
        raise ValueError("Không tìm thấy camera")

    bbox = _bbox_payload(payload.bbox)
    if bbox["x"] + bbox["w"] > 1.000001 or bbox["y"] + bbox["h"] > 1.000001:
        raise ValueError("BBox vượt quá khung ảnh (tọa độ chuẩn hóa 0–1)")

    detection = AiDetection(
        id=new_detection_id(),
        camera_id=camera_id,
        label=payload.label,
        confidence=float(payload.confidence),
        bbox=bbox,
        created_at=utc_now_iso(),
    )
    db.add(detection)
    db.commit()
    db.refresh(detection)
    return detection

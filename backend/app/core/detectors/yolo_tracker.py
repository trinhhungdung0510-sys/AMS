from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any, Optional

from app.core.detectors.yolo_class_mapper import map_yolo_class


@dataclass
class DetectionInput:
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float
    class_name: str


@dataclass
class TrackedDetection:
    track_id: str
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float
    ams_class: str
    tracker: str


def _iou(a: DetectionInput, b: "TrackedBox") -> float:
    ix1 = max(a.x1, b.x1)
    iy1 = max(a.y1, b.y1)
    ix2 = min(a.x2, b.x2)
    iy2 = min(a.y2, b.y2)
    inter = max(0.0, ix2 - ix1) * max(0.0, iy2 - iy1)
    if inter <= 0:
        return 0.0
    area_a = max(0.0, a.x2 - a.x1) * max(0.0, a.y2 - a.y1)
    area_b = max(0.0, b.x2 - b.x1) * max(0.0, b.y2 - b.y1)
    union = area_a + area_b - inter
    return inter / union if union > 0 else 0.0


@dataclass
class TrackedBox:
    track_id: str
    x1: float
    y1: float
    x2: float
    y2: float
    ams_class: str
    misses: int = 0


class SimpleTrackTracker:
    """Fallback tracker when ByteTrack/supervision is unavailable."""

    def __init__(self, iou_threshold: float = 0.3, max_misses: int = 15) -> None:
        self._tracks: dict[str, TrackedBox] = {}
        self._iou_threshold = iou_threshold
        self._max_misses = max_misses
        self._counter = 0

    @property
    def backend_name(self) -> str:
        return "simple"

    def update(self, detections: list[DetectionInput]) -> list[TrackedDetection]:
        assigned: set[str] = set()
        outputs: list[TrackedDetection] = []

        for detection in detections:
            ams_class = map_yolo_class(detection.class_name)
            if not ams_class:
                continue

            best_id: Optional[str] = None
            best_iou = 0.0
            for track_id, track in self._tracks.items():
                if track_id in assigned or track.ams_class != ams_class:
                    continue
                score = _iou(detection, track)
                if score >= self._iou_threshold and score > best_iou:
                    best_iou = score
                    best_id = track_id

            if best_id:
                track = self._tracks[best_id]
                track.x1, track.y1, track.x2, track.y2 = (
                    detection.x1,
                    detection.y1,
                    detection.x2,
                    detection.y2,
                )
                track.misses = 0
                assigned.add(best_id)
                track_id = best_id
            else:
                self._counter += 1
                track_id = f"TMP-{self._counter:05d}"
                self._tracks[track_id] = TrackedBox(
                    track_id=track_id,
                    x1=detection.x1,
                    y1=detection.y1,
                    x2=detection.x2,
                    y2=detection.y2,
                    ams_class=ams_class,
                )
                assigned.add(track_id)

            outputs.append(
                TrackedDetection(
                    track_id=track_id,
                    x1=detection.x1,
                    y1=detection.y1,
                    x2=detection.x2,
                    y2=detection.y2,
                    confidence=detection.confidence,
                    ams_class=ams_class,
                    tracker=self.backend_name,
                )
            )

        for track_id, track in list(self._tracks.items()):
            if track_id in assigned:
                continue
            track.misses += 1
            if track.misses > self._max_misses:
                del self._tracks[track_id]

        return outputs


class ByteTrackWrapper:
    """ByteTrack via supervision when installed."""

    def __init__(self) -> None:
        import numpy as np
        import supervision as sv

        self._np = np
        self._tracker = sv.ByteTrack()
        self._sv = sv

    @property
    def backend_name(self) -> str:
        return "bytetrack"

    def update(self, detections: list[DetectionInput]) -> list[TrackedDetection]:
        if not detections:
            return []

        xyxy = []
        confidences = []
        class_ids = []
        class_names = []
        for item in detections:
            ams_class = map_yolo_class(item.class_name)
            if not ams_class:
                continue
            xyxy.append([item.x1, item.y1, item.x2, item.y2])
            confidences.append(item.confidence)
            class_ids.append(0 if ams_class == "person" else 1)
            class_names.append(ams_class)

        if not xyxy:
            return []

        detections_sv = self._sv.Detections(
            xyxy=self._np.array(xyxy, dtype=float),
            confidence=self._np.array(confidences, dtype=float),
            class_id=self._np.array(class_ids, dtype=int),
        )
        tracked = self._tracker.update_with_detections(detections_sv)
        outputs: list[TrackedDetection] = []

        for index in range(len(tracked)):
            track_id_raw = tracked.tracker_id[index] if tracked.tracker_id is not None else None
            track_id = f"BT-{int(track_id_raw):05d}" if track_id_raw is not None else f"TMP-{uuid.uuid4().hex[:8]}"
            x1, y1, x2, y2 = tracked.xyxy[index]
            class_id = int(tracked.class_id[index]) if tracked.class_id is not None else 0
            ams_class = class_names[index] if index < len(class_names) else ("person" if class_id == 0 else "animal")
            confidence = float(tracked.confidence[index]) if tracked.confidence is not None else 0.0
            outputs.append(
                TrackedDetection(
                    track_id=track_id,
                    x1=float(x1),
                    y1=float(y1),
                    x2=float(x2),
                    y2=float(y2),
                    confidence=confidence,
                    ams_class=ams_class,
                    tracker=self.backend_name,
                )
            )
        return outputs


def create_tracker(prefer_bytetrack: bool = True) -> Any:
    if prefer_bytetrack:
        try:
            return ByteTrackWrapper()
        except ImportError:
            pass
    return SimpleTrackTracker()


def is_bytetrack_available() -> bool:
    try:
        import supervision  # noqa: F401

        return True
    except ImportError:
        return False

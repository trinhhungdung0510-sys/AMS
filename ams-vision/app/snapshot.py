from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy as np

from app.detector import Detection

SEVERITY_COLORS = {
    "critical": (38, 38, 220),
    "high": (12, 88, 234),
    "warning": (4, 138, 202),
    "danger": (38, 38, 220),
    "info": (235, 99, 37),
}


class SnapshotService:
    def __init__(self, snapshots_dir: str) -> None:
        self.snapshots_dir = Path(snapshots_dir)
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)
        self.thumbs_dir = self.snapshots_dir / "thumbs"
        self.thumbs_dir.mkdir(parents=True, exist_ok=True)

    def create_mock_frame(self) -> np.ndarray:
        frame = np.zeros((720, 1280, 3), dtype=np.uint8)
        frame[:] = (28, 72, 38)
        cv2.putText(
            frame,
            "AMS Vision Camera Feed",
            (48, 48),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (187, 247, 208),
            2,
        )
        return frame

    def save_violation_snapshot(
        self,
        frame: np.ndarray,
        detection: Detection,
        camera_id: str,
        *,
        zone_name: str = "Unknown Zone",
        rule_name: str = "AI Detection Rule",
        timestamp: str | None = None,
        severity: str = "warning",
        track_id: int | None = None,
    ) -> str:
        annotated = self.render_annotated_snapshot(
            frame,
            detection,
            zone_name=zone_name,
            rule_name=rule_name,
            timestamp=timestamp or datetime.now(timezone.utc).isoformat(),
            severity=severity,
            track_id=track_id,
        )
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path = self.snapshots_dir / f"{camera_id}_{stamp}_{detection.label}.jpg"
        thumb_path = self.thumbs_dir / f"{camera_id}_{stamp}_{detection.label}.jpg"
        cv2.imwrite(str(path), annotated, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
        thumb = cv2.resize(annotated, (320, int(annotated.shape[0] * (320 / annotated.shape[1]))))
        cv2.imwrite(str(thumb_path), thumb, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        return str(path)

    def render_annotated_snapshot(
        self,
        frame: np.ndarray,
        detection: Detection,
        *,
        zone_name: str,
        rule_name: str,
        timestamp: str,
        severity: str,
        track_id: int | None = None,
    ) -> np.ndarray:
        annotated = frame.copy()
        x1, y1, x2, y2 = detection.bbox
        color = SEVERITY_COLORS.get(severity.lower(), (235, 99, 37))

        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 3)
        cv2.rectangle(annotated, (x1 + 2, y1 + 2), (x2 - 2, y2 - 2), (255, 255, 255), 1)

        label = detection.label
        if track_id is not None:
            label = f"{label} #{track_id}"
        label = f"{label} {detection.confidence:.0f}%"
        tag_y1 = max(0, y1 - 34)
        cv2.rectangle(annotated, (x1, tag_y1), (x1 + max(180, len(label) * 12), y1), color, -1)
        cv2.putText(
            annotated,
            label,
            (x1 + 8, max(22, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2,
        )

        panel_top = annotated.shape[0] - 150
        cv2.rectangle(annotated, (0, panel_top), (annotated.shape[1], annotated.shape[0]), (42, 23, 15), -1)
        cv2.rectangle(annotated, (0, panel_top), (annotated.shape[1], panel_top + 4), color, -1)

        display_time = timestamp.replace("T", " ").replace("+00:00", " UTC")[:32]
        lines = [
            ("Zone", zone_name),
            ("Rule", rule_name),
            ("Time", display_time),
            ("Severity", severity.upper()),
        ]
        y = panel_top + 24
        for label_key, value in lines:
            cv2.putText(
                annotated,
                f"{label_key}:",
                (24, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (148, 163, 184),
                1,
            )
            value_color = color if label_key == "Severity" else (252, 250, 248)
            cv2.putText(
                annotated,
                value[:72],
                (120, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                value_color,
                2,
            )
            y += 30

        cv2.putText(
            annotated,
            "AMS Snapshot v3.5",
            (annotated.shape[1] - 240, 28),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (148, 163, 184),
            2,
        )
        return annotated

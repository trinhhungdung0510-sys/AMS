import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional

import cv2

from app.config import VisionSettings
from app.detector import YOLODetector
from app.publisher import EventPublisher
from app.snapshot import SnapshotService
from app.tracking import TrackingEngine

logger = logging.getLogger("ams-vision")


class RTSPStreamWorker:
    def __init__(self, settings: VisionSettings) -> None:
        self.settings = settings
        self.detector = YOLODetector(settings.yolo_model, mock=settings.mock_detection)
        self.snapshots = SnapshotService(settings.snapshots_dir)
        self.publisher = EventPublisher(settings.backend_base_url)
        self.tracking = TrackingEngine(
            settings.backend_base_url,
            settings.camera_id,
            settings.track_history_path,
        )
        self.last_detection: Optional[dict] = None
        self.detections_published = 0

    def _read_rtsp_frame(self):
        capture = cv2.VideoCapture(self.settings.rtsp_url)
        try:
            ok, frame = capture.read()
            if not ok:
                raise RuntimeError("Unable to read RTSP frame")
            return frame
        finally:
            capture.release()

    async def run_once(self) -> dict:
        frame = (
            self.snapshots.create_mock_frame()
            if self.settings.mock_detection
            else await asyncio.to_thread(self._read_rtsp_frame)
        )
        detections = self.detector.detect(frame)
        tracks = self.tracking.update(detections)
        published_transitions = []
        for transition in self.tracking.latest_transitions:
            try:
                published = self.publisher.publish_crossing(
                    track_id=transition["track_id"],
                    camera_id=self.settings.camera_id,
                    zone_id=transition["to_zone"],
                    timestamp=transition["timestamp"],
                    object_type=transition["object_type"],
                )
                if published:
                    published_transitions.append(published)
            except Exception as exc:
                logger.exception("Failed to publish zone crossing: %s", exc)

        synced_tracks = []
        if tracks:
            try:
                synced_tracks = self.publisher.sync_tracks(
                    [
                        {
                            "track_id": track.track_id,
                            "camera_id": track.camera_id,
                            "object_type": track.object_type,
                            "current_zone": track.current_zone,
                            "previous_zone": track.previous_zone,
                            "enter_time": track.enter_time,
                            "leave_time": track.leave_time,
                            "last_seen": track.last_seen,
                            "confidence": track.confidence,
                        }
                        for track in tracks
                    ]
                )
            except Exception as exc:
                logger.exception("Failed to sync tracks with backend: %s", exc)

        if not detections:
            result = {
                "status": "no_detection",
                "tracks": synced_tracks or [],
                "transitions": published_transitions,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            self.last_detection = result
            return result

        detection = detections[0]
        track = tracks[0] if tracks else None
        snapshot_path = self.snapshots.save_violation_snapshot(
            frame,
            detection,
            self.settings.camera_id,
            zone_name=track.current_zone if track else "Unknown Zone",
            rule_name=self.settings.publish_category,
            severity="critical" if detection.label in {"dog", "rat"} else "warning",
            track_id=track.track_id if track else None,
        )
        backend_task = self.publisher.publish_detection(
            camera_id=self.settings.camera_id,
            category=self.settings.publish_category,
            priority=9,
        )
        self.detections_published += 1
        result = {
            "status": "published",
            "camera_id": self.settings.camera_id,
            "label": detection.label,
            "confidence": detection.confidence,
            "snapshot_path": snapshot_path,
            "backend_task_id": backend_task["id"],
            "backend_task_status": backend_task["status"],
            "tracks": synced_tracks
            or [
                {
                    "track_id": track.track_id,
                    "camera_id": track.camera_id,
                    "object_type": track.object_type,
                    "current_zone": track.current_zone,
                    "previous_zone": track.previous_zone,
                    "enter_time": track.enter_time,
                    "leave_time": track.leave_time,
                }
                for track in tracks
            ],
            "transitions": published_transitions,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.last_detection = result
        return result

    async def run_forever(self, stop_event: asyncio.Event) -> None:
        while not stop_event.is_set():
            try:
                await self.run_once()
            except Exception as exc:
                logger.exception("Vision worker pipeline failed: %s", exc)
                self.last_detection = {
                    "status": "error",
                    "error": str(exc),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }

            try:
                await asyncio.wait_for(
                    stop_event.wait(),
                    timeout=self.settings.mock_detection_interval,
                )
            except asyncio.TimeoutError:
                continue

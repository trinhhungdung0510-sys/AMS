from dataclasses import dataclass
from typing import Any, Optional

import numpy as np

TARGET_CLASSES = {"person", "dog", "cat", "bird", "car", "motorcycle", "bus", "truck"}
VEHICLE_CLASSES = {"car", "motorcycle", "bus", "truck"}


@dataclass
class Detection:
    label: str
    confidence: float
    bbox: tuple[int, int, int, int]
    track_id: Optional[int] = None


class YOLODetector:
    def __init__(self, model_name: str, mock: bool = True) -> None:
        self.model_name = model_name
        self.mock = mock
        self._model: Any = None
        self._mock_step = 0

    def _load_model(self) -> None:
        if self._model is None:
            from ultralytics import YOLO

            self._model = YOLO(self.model_name)

    def detect(self, frame: np.ndarray) -> list[Detection]:
        if self.mock:
            height, width = frame.shape[:2]
            self._mock_step += 1
            person_x = min(width - 280, 80 + self._mock_step * 90)
            dog_x = min(width - 180, 390 + self._mock_step * 45)
            return [
                Detection(
                    label="person",
                    confidence=0.93,
                    bbox=(person_x, height // 6, person_x + 190, (height * 3) // 4),
                    track_id=1,
                ),
                Detection(
                    label="dog",
                    confidence=0.88,
                    bbox=(dog_x, height // 3, dog_x + 130, height // 2),
                    track_id=2,
                ),
                Detection(
                    label="vehicle",
                    confidence=0.91,
                    bbox=(430, 300, 720, 510),
                    track_id=3,
                ),
            ]

        self._load_model()
        results = self._model.track(frame, tracker="bytetrack.yaml", persist=True, verbose=False)
        detections: list[Detection] = []
        for result in results:
            names = result.names
            for box in result.boxes:
                label = names[int(box.cls[0])]
                if label not in TARGET_CLASSES:
                    continue
                normalized_label = "vehicle" if label in VEHICLE_CLASSES else label
                x1, y1, x2, y2 = [int(value) for value in box.xyxy[0].tolist()]
                track_id = int(box.id[0]) if box.id is not None else None
                detections.append(
                    Detection(
                        label=normalized_label,
                        confidence=float(box.conf[0]),
                        bbox=(x1, y1, x2, y2),
                        track_id=track_id,
                    )
                )
        return detections

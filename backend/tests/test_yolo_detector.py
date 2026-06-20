import unittest

from app.core.detectors.yolo_class_mapper import (
    COCO_BIRD,
    COCO_CAT,
    COCO_DOG,
    COCO_PERSON,
    SUPPORTED_COCO_CLASS_IDS,
    map_coco_class_id,
    map_yolo_class,
)
from app.core.detectors.yolo_observation_mapper import (
    build_observation_payload,
    normalize_bbox_xyxy,
)
from app.core.detectors.yolo_detector_adapter import parse_video_source
from app.core.detectors.yolo_tracker import DetectionInput, SimpleTrackTracker
from app.services.observation_validator import observation_validator


class YoloClassMapperTest(unittest.TestCase):
    def test_person_maps_to_person(self) -> None:
        self.assertEqual(map_yolo_class("person"), "person")
        self.assertEqual(map_yolo_class("PERSON"), "person")

    def test_animals_map_to_animal(self) -> None:
        for label in ("dog", "cat", "bird", "Dog", "CAT"):
            self.assertEqual(map_yolo_class(label), "animal")

    def test_unknown_returns_none(self) -> None:
        self.assertIsNone(map_yolo_class("car"))

    def test_coco_ids(self) -> None:
        names = {COCO_PERSON: "person", COCO_BIRD: "bird", COCO_DOG: "dog", COCO_CAT: "cat"}
        self.assertEqual(map_coco_class_id(COCO_DOG, names), "animal")
        self.assertEqual(len(SUPPORTED_COCO_CLASS_IDS), 4)


class YoloObservationMapperTest(unittest.TestCase):
    def test_normalize_bbox(self) -> None:
        bbox = normalize_bbox_xyxy(100, 200, 300, 500, 1920, 1080)
        self.assertAlmostEqual(bbox["x"], 100 / 1920, places=4)
        self.assertAlmostEqual(bbox["y"], 200 / 1080, places=4)
        self.assertAlmostEqual(bbox["width"], 200 / 1920, places=4)
        self.assertAlmostEqual(bbox["height"], 300 / 1080, places=4)

    def test_payload_validates(self) -> None:
        payload = build_observation_payload(
            camera_id="CAM-TEST",
            objects=[
                {
                    "trackId": "BT-00001",
                    "class": "person",
                    "confidence": 0.91,
                    "bbox": {"x": 0.1, "y": 0.2, "width": 0.15, "height": 0.4},
                    "attributes": {"tracker": "bytetrack"},
                }
            ],
            frame_width=1280,
            frame_height=720,
            source="YOLO",
        )
        validated = observation_validator.validate(payload)
        self.assertEqual(validated.source, "YOLO")
        self.assertEqual(validated.objects[0].object_class, "person")


class ParseVideoSourceTest(unittest.TestCase):
    def test_webcam_aliases(self) -> None:
        self.assertEqual(parse_video_source("webcam"), 0)
        self.assertEqual(parse_video_source("webcam:1"), 1)
        self.assertEqual(parse_video_source("0"), 0)

    def test_rtsp_and_file(self) -> None:
        url = "rtsp://192.168.1.5/stream"
        self.assertEqual(parse_video_source(url), url)
        self.assertEqual(parse_video_source("/tmp/sample.mp4"), "/tmp/sample.mp4")


class SimpleTrackerTest(unittest.TestCase):
    def test_assigns_stable_track_ids(self) -> None:
        tracker = SimpleTrackTracker()
        first = tracker.update(
            [
                DetectionInput(
                    x1=10,
                    y1=10,
                    x2=50,
                    y2=80,
                    confidence=0.9,
                    class_name="person",
                )
            ]
        )
        second = tracker.update(
            [
                DetectionInput(
                    x1=12,
                    y1=11,
                    x2=52,
                    y2=82,
                    confidence=0.88,
                    class_name="person",
                )
            ]
        )
        self.assertEqual(len(first), 1)
        self.assertEqual(len(second), 1)
        self.assertEqual(first[0].track_id, second[0].track_id)
        self.assertEqual(first[0].ams_class, "person")


if __name__ == "__main__":
    unittest.main()

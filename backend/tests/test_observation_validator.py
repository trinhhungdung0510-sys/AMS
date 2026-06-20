import unittest

from app.services.observation_validator import observation_validator


class ObservationValidatorTest(unittest.TestCase):
    def test_valid_v1_payload(self) -> None:
        payload = {
            "schemaVersion": "v1",
            "cameraId": "CAM-1",
            "timestamp": "2026-06-23T10:00:00+00:00",
            "source": "MOCK",
            "frameWidth": 1920,
            "frameHeight": 1080,
            "objects": [
                {
                    "trackId": "T-1",
                    "class": "person",
                    "confidence": 0.9,
                    "bbox": {"x": 0.1, "y": 0.2, "width": 0.15, "height": 0.3},
                }
            ],
        }
        result = observation_validator.validate(payload)
        self.assertEqual(result.schema_version, "v1")
        self.assertEqual(result.camera_id, "CAM-1")

    def test_rejects_missing_track_id(self) -> None:
        payload = {
            "cameraId": "CAM-1",
            "timestamp": "2026-06-23T10:00:00+00:00",
            "source": "MOCK",
            "frameWidth": 1920,
            "frameHeight": 1080,
            "objects": [{"class": "person", "confidence": 0.9, "bbox": {"x": 0.1, "y": 0.2, "width": 0.1, "height": 0.2}}],
        }
        with self.assertRaises(ValueError):
            observation_validator.validate(payload)

    def test_rejects_invalid_schema_version(self) -> None:
        payload = {
            "schemaVersion": "v99",
            "cameraId": "CAM-1",
            "timestamp": "2026-06-23T10:00:00+00:00",
            "source": "MOCK",
            "frameWidth": 1920,
            "frameHeight": 1080,
            "objects": [],
        }
        with self.assertRaises(ValueError):
            observation_validator.validate(payload)


if __name__ == "__main__":
    unittest.main()

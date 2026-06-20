import unittest

from pydantic import ValidationError

from app.schemas.observation import BboxNormalized, ObservationCreate, ObservationObject


class ObservationSchemaValidationTest(unittest.TestCase):
    def test_valid_observation(self):
        payload = ObservationCreate(
            cameraId="CAM-001",
            timestamp="2026-06-22T10:00:00+00:00",
            source="MOCK",
            frameWidth=1920,
            frameHeight=1080,
            objects=[
                ObservationObject(
                    trackId="T-1",
                    **{"class": "person"},
                    confidence=0.95,
                    bbox=BboxNormalized(x=0.1, y=0.2, width=0.15, height=0.3),
                    attributes={"helmet": True},
                )
            ],
        )
        self.assertEqual(payload.camera_id, "CAM-001")
        self.assertEqual(payload.source, "MOCK")

    def test_rejects_invalid_source(self):
        with self.assertRaises(ValidationError):
            ObservationCreate(
                cameraId="CAM-001",
                timestamp="2026-06-22T10:00:00+00:00",
                source="INVALID",
                frameWidth=1920,
                frameHeight=1080,
                objects=[],
            )

    def test_rejects_bbox_out_of_bounds(self):
        with self.assertRaises(ValidationError):
            BboxNormalized(x=0.9, y=0.2, width=0.2, height=0.3)


if __name__ == "__main__":
    unittest.main()

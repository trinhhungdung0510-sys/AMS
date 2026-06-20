import unittest

from app.core.detectors import MockDetectorAdapter, get_detector_registry
from app.core.detectors.detector_registry import DetectorRegistry


class DetectorRegistryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = DetectorRegistry()

    def test_register_get_list_unregister(self) -> None:
        detector = MockDetectorAdapter()
        self.registry.register(detector)

        self.assertIs(self.registry.get("mock-detector-v1"), detector)
        self.assertEqual(len(self.registry.list()), 1)

        removed = self.registry.unregister("mock-detector-v1")
        self.assertTrue(removed)
        self.assertIsNone(self.registry.get("mock-detector-v1"))

    def test_singleton_registry(self) -> None:
        registry = get_detector_registry()
        self.assertIsNotNone(registry)


if __name__ == "__main__":
    unittest.main()

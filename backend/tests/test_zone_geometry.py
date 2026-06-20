import unittest

from app.utils.zone_geometry import (
    denormalize_point,
    normalize_point,
    resolve_normalized_points,
    scale_polygon_to_normalized,
)


class ZoneGeometryTests(unittest.TestCase):
    def test_normalize_point(self):
        self.assertEqual(
            normalize_point({"x": 192, "y": 108}, 1920, 1080),
            {"x": 0.1, "y": 0.1},
        )

    def test_denormalize_point(self):
        self.assertEqual(
            denormalize_point({"x": 0.25, "y": 0.5}, 1920, 1080),
            {"x": 480.0, "y": 540.0},
        )

    def test_scale_polygon_to_normalized(self):
        polygon = [
            {"x": 0, "y": 0},
            {"x": 1920, "y": 0},
            {"x": 960, "y": 1080},
        ]
        self.assertEqual(
            scale_polygon_to_normalized(polygon, 1920, 1080),
            [
                {"x": 0.0, "y": 0.0},
                {"x": 1.0, "y": 0.0},
                {"x": 0.5, "y": 1.0},
            ],
        )

    def test_resolve_legacy_pixel_zone(self):
        points = [{"x": 960, "y": 540}]
        resolved = resolve_normalized_points(
            points,
            points_format="pixel",
            reference_width=1920,
            reference_height=1080,
        )
        self.assertEqual(resolved, [{"x": 0.5, "y": 0.5}])


if __name__ == "__main__":
    unittest.main()

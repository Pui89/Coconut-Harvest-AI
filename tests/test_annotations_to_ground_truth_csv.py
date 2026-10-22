"""Unit tests for normalized annotation to pixel-coordinate CSV conversion."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "annotations_to_ground_truth_csv.py"
SPEC = importlib.util.spec_from_file_location("annotations_to_ground_truth_csv", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class AnnotationConversionTests(unittest.TestCase):
    def setUp(self):
        self.payload = {
            "format": "pui89-coconut-annotations-v1",
            "images": [
                {
                    "filename": "orchard_a.jpg",
                    "width": 100,
                    "height": 200,
                    "boxes": [{"x": 0.1, "y": 0.2, "w": 0.3, "h": 0.4}],
                },
                {"filename": "empty.jpg", "width": 50, "height": 60, "boxes": []},
            ],
        }

    def test_converts_normalized_box_to_pixel_coordinates(self):
        rows, summary = MODULE.convert(self.payload, None, True)
        self.assertEqual(rows, [{
            "image_id": "orchard_a.jpg",
            "xmin": "10.0",
            "ymin": "40.0",
            "xmax": "40.0",
            "ymax": "120.0",
            "class": "coconut",
        }])
        self.assertEqual(summary["image_count"], 2)
        self.assertEqual(summary["box_count"], 1)
        self.assertEqual(summary["images_with_zero_boxes"], 1)
        self.assertTrue(summary["human_qa_acknowledged"])

    def test_rejects_invalid_box_geometry(self):
        self.payload["images"][0]["boxes"][0]["w"] = 0
        with self.assertRaisesRegex(ValueError, "outside normalized image bounds"):
            MODULE.convert(self.payload, None, True)

    def test_rejects_duplicate_filenames_case_insensitively(self):
        self.payload["images"][1]["filename"] = "ORCHARD_A.jpg"
        with self.assertRaisesRegex(ValueError, "duplicate image filename"):
            MODULE.convert(self.payload, None, True)

    def test_does_not_claim_qa_was_done_by_itself(self):
        _, summary = MODULE.convert(self.payload, None, False)
        self.assertFalse(summary["human_qa_acknowledged"])
        self.assertFalse(summary["evaluator_csv_written"])

    def test_rejects_wrong_format(self):
        self.payload["format"] = "other"
        with self.assertRaisesRegex(ValueError, "expected annotation JSON format"):
            MODULE.convert(self.payload, None, True)


    def test_rejects_non_finite_coordinates(self):
        self.payload["images"][0]["boxes"][0]["x"] = float("nan")
        with self.assertRaisesRegex(ValueError, "finite numbers"):
            MODULE.convert(self.payload, None, True)

    def test_rejects_non_integer_image_dimensions(self):
        self.payload["images"][0]["width"] = 100.5
        with self.assertRaisesRegex(ValueError, "must be integers"):
            MODULE.convert(self.payload, None, True)

    def test_rejects_path_traversal_filename(self):
        self.payload["images"][0]["filename"] = "../orchard_a.jpg"
        with self.assertRaisesRegex(ValueError, "must be a basename"):
            MODULE.convert(self.payload, None, True)

    def test_rejects_missing_image_file_when_directory_is_supplied(self):
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as temp_dir:
            with self.assertRaisesRegex(ValueError, "image file not found"):
                MODULE.convert(self.payload, Path(temp_dir), True)


if __name__ == "__main__":
    unittest.main()

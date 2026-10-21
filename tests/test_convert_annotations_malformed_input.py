"""Regression tests for malformed annotation JSON handling."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "convert_annotations_to_yolo.py"


class AnnotationConverterMalformedInputTests(unittest.TestCase):
    def run_converter(self, payload):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            annotations = root / "annotations.json"
            annotations.write_text(json.dumps(payload), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--annotations", str(annotations),
                 "--output-dir", str(root / "out")],
                capture_output=True, text=True, check=False,
            )
            return result

    def test_rejects_non_object_json_root_without_traceback(self):
        result = self.run_converter([])
        self.assertEqual(result.returncode, 2)
        self.assertIn("top level must be an object", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_rejects_non_object_image_record_without_traceback(self):
        result = self.run_converter({"format": "pui89-coconut-annotations-v1", "images": [None]})
        self.assertEqual(result.returncode, 2)
        self.assertIn("image record 1 must be an object", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_rejects_non_list_boxes_without_traceback(self):
        result = self.run_converter({
            "format": "pui89-coconut-annotations-v1",
            "images": [{"filename": "sample.jpg", "boxes": {}}],
        })
        self.assertEqual(result.returncode, 2)
        self.assertIn("boxes for image record must be a list", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()

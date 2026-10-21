"""Tests for the local YOLO dataset validator."""
import tempfile
import unittest
from pathlib import Path

from apps.pui89_app.validate_coconut_dataset import validate_dataset


class ValidateDatasetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for split in ("train", "val", "test"):
            (self.root / "images" / split).mkdir(parents=True)
            (self.root / "labels" / split).mkdir(parents=True)

    def add_pair(self, split="train", label="0 0.5 0.5 0.2 0.3\n"):
        (self.root / "images" / split / "sample.jpg").write_bytes(b"test image placeholder")
        (self.root / "labels" / split / "sample.txt").write_text(label, encoding="utf-8")

    def test_valid_normalized_box_passes(self):
        self.add_pair()
        report = validate_dataset(self.root, class_count=1, splits=("train",))
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["splits"]["train"]["objects"], 1)

    def test_out_of_range_class_fails(self):
        self.add_pair(label="1 0.5 0.5 0.2 0.3\n")
        report = validate_dataset(self.root, class_count=1, splits=("train",))
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("class_id" in error["message"] for error in report["errors"]))

    def test_missing_label_fails(self):
        (self.root / "images" / "train" / "unlabelled.jpg").write_bytes(b"test")
        report = validate_dataset(self.root, class_count=1, splits=("train",))
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("Missing matching label" in error["message"] for error in report["errors"]))

    def test_box_outside_image_fails(self):
        self.add_pair(label="0 0.95 0.5 0.2 0.3\n")
        report = validate_dataset(self.root, class_count=1, splits=("train",))
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("extends beyond" in error["message"] for error in report["errors"]))

    def test_empty_label_file_is_valid_negative_example(self):
        self.add_pair(label="")
        report = validate_dataset(self.root, class_count=1, splits=("train",))
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["splits"]["train"]["empty_label_files"], 1)


if __name__ == "__main__":
    unittest.main()

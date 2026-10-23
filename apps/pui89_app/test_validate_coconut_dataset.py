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

    def test_exact_duplicate_image_across_splits_fails(self):
        self.add_pair(split="train")
        # Same bytes under a different filename must not leak into validation.
        (self.root / "images" / "val" / "copy.jpg").write_bytes(b"test image placeholder")
        (self.root / "labels" / "val" / "copy.txt").write_text(
            "0 0.5 0.5 0.2 0.3\\n", encoding="utf-8"
        )
        report = validate_dataset(self.root, class_count=1)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any(
            "Exact duplicate image content appears in split" in error["message"]
            for error in report["errors"]
        ))

    def test_exact_duplicate_within_split_is_warning_not_cross_split_failure(self):
        self.add_pair(split="train")
        (self.root / "images" / "train" / "copy.jpg").write_bytes(
            b"test image placeholder"
        )
        (self.root / "labels" / "train" / "copy.txt").write_text(
            "0 0.5 0.5 0.2 0.3\\n", encoding="utf-8"
        )
        report = validate_dataset(self.root, class_count=1, splits=("train",))
        self.assertEqual(report["status"], "PASS")
        self.assertTrue(any("Exact duplicate image content within" in warning
                            for warning in report["warnings"]))

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

    def test_unreadable_utf8_label_is_reported_without_crashing(self):
        self.add_pair()
        label_path = self.root / "labels" / "train" / "sample.txt"
        label_path.write_bytes(b"\xff\xfe\xfa")
        report = validate_dataset(self.root, class_count=1, splits=("train",))
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("Cannot read label file" in error["message"] for error in report["errors"]))
        self.assertEqual(report["splits"]["train"]["empty_label_files"], 0)


if __name__ == "__main__":
    unittest.main()

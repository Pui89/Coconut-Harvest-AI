"""Edge cases for the dataset split leakage release gate.

These tests validate manifest bookkeeping only; they do not validate image
content, annotation quality, dataset licensing, or model performance.
"""
import csv
import tempfile
import unittest
from pathlib import Path

from tools.audit_dataset_split_leakage import audit_manifest

FIELDS = ["image_id", "filename", "split", "group_id", "sha256"]
HASH_A = "a" * 64
HASH_B = "b" * 64


def write_manifest(rows):
    temp = tempfile.TemporaryDirectory()
    path = Path(temp.name) / "manifest.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return temp, path


def row(image_id, filename, split, group_id, sha256):
    return dict(image_id=image_id, filename=filename, split=split, group_id=group_id, sha256=sha256)


class SplitLeakageAuditEdgeCaseTests(unittest.TestCase):
    def test_header_only_manifest_does_not_pass(self):
        temp, path = write_manifest([])
        self.addCleanup(temp.cleanup)
        report = audit_manifest(path)
        self.assertFalse(report["passed"])
        self.assertEqual(report["row_count"], 0)

    def test_duplicate_image_id_is_rejected_case_insensitively(self):
        temp, path = write_manifest([
            row("Palm-01", "one.jpg", "train", "session-1", HASH_A),
            row("palm-01", "two.jpg", "test", "session-2", HASH_B),
        ])
        self.addCleanup(temp.cleanup)
        report = audit_manifest(path)
        self.assertFalse(report["passed"])
        self.assertTrue(any("duplicate image_id" in error for error in report["errors"]))

    def test_group_id_case_variation_cannot_cross_splits(self):
        temp, path = write_manifest([
            row("one", "one.jpg", "train", "Orchard-Session-A", HASH_A),
            row("two", "two.jpg", "test", "orchard-session-a", HASH_B),
        ])
        self.addCleanup(temp.cleanup)
        report = audit_manifest(path)
        self.assertFalse(report["passed"])
        self.assertEqual(len(report["group_cross_split_findings"]), 1)


if __name__ == "__main__":
    unittest.main()

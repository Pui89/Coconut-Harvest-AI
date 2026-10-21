import csv
import tempfile
import unittest
from pathlib import Path

from tools.audit_dataset_split_leakage import audit_manifest


FIELDS = ["image_id", "filename", "split", "group_id", "sha256"]
HASH_A = "a" * 64
HASH_B = "b" * 64


class SplitLeakageAuditTests(unittest.TestCase):
    def write_manifest(self, rows):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "manifest.csv"
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        return path

    def row(self, image_id, filename, split, group_id, sha256):
        return dict(image_id=image_id, filename=filename, split=split, group_id=group_id, sha256=sha256)

    def test_clean_grouped_split_passes(self):
        path = self.write_manifest([
            self.row("a", "a.jpg", "train", "session-1", HASH_A),
            self.row("b", "b.jpg", "test", "session-2", HASH_B),
        ])
        report = audit_manifest(path)
        self.assertTrue(report["passed"])
        self.assertEqual(report["split_counts"]["train"], 1)

    def test_same_hash_across_splits_fails(self):
        path = self.write_manifest([
            self.row("a", "a.jpg", "train", "session-1", HASH_A),
            self.row("b", "b-copy.jpg", "test", "session-2", HASH_A),
        ])
        report = audit_manifest(path)
        self.assertFalse(report["passed"])
        self.assertEqual(len(report["identical_hash_cross_split_findings"]), 1)

    def test_same_group_across_splits_fails(self):
        path = self.write_manifest([
            self.row("a", "a.jpg", "train", "same-orchard-session", HASH_A),
            self.row("b", "b.jpg", "validation", "same-orchard-session", HASH_B),
        ])
        report = audit_manifest(path)
        self.assertFalse(report["passed"])
        self.assertEqual(len(report["group_cross_split_findings"]), 1)

    def test_duplicate_filename_fails_case_insensitively(self):
        path = self.write_manifest([
            self.row("a", "Coconut.jpg", "train", "session-1", HASH_A),
            self.row("b", "coconut.JPG", "test", "session-2", HASH_B),
        ])
        self.assertFalse(audit_manifest(path)["passed"])

    def test_invalid_hash_and_unassigned_split_fail(self):
        path = self.write_manifest([
            self.row("a", "a.jpg", "unassigned", "session-1", "not-a-hash"),
        ])
        report = audit_manifest(path)
        self.assertFalse(report["passed"])
        self.assertTrue(any("sha256" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()

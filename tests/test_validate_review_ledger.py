import csv
import tempfile
import unittest
from pathlib import Path

from tools.validate_review_ledger import validate

FIELDS = [
    "candidate_id", "filename", "decision", "reason_code", "reviewer",
    "reviewed_on", "source_url", "rights_status", "annotation_status", "split",
]


def row(**overrides):
    values = {
        "candidate_id": "0001", "filename": "coconut.jpg", "decision": "approved",
        "reason_code": "", "reviewer": "reviewer-a", "reviewed_on": "2026-10-21",
        "source_url": "https://example.org/source", "rights_status": "cleared",
        "annotation_status": "reviewed", "split": "train",
    }
    values.update(overrides)
    return values


class ReviewLedgerValidationTests(unittest.TestCase):
    def check_rows(self, rows):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(rows)
            return validate(path)

    def test_valid_approved_candidate_passes(self):
        self.assertEqual(self.check_rows([row()]), [])

    def test_duplicate_ids_and_case_insensitive_filenames_fail(self):
        errors = self.check_rows([row(), row(filename="COCONUT.JPG")])
        self.assertTrue(any("duplicate candidate_id" in error for error in errors))
        self.assertTrue(any("duplicate filename" in error for error in errors))

    def test_approved_candidate_requires_rights_and_annotation_gates(self):
        errors = self.check_rows([row(rights_status="unresolved", annotation_status="unreviewed")])
        self.assertTrue(any("rights_status=cleared" in error for error in errors))
        self.assertTrue(any("annotation_status=reviewed" in error for error in errors))

    def test_quarantine_requires_reason(self):
        errors = self.check_rows([row(decision="quarantine_rights", reason_code="")])
        self.assertTrue(any("requires reason_code" in error for error in errors))

    def test_unknown_decision_is_rejected(self):
        errors = self.check_rows([row(decision="maybe")])
        self.assertTrue(any("invalid decision" in error for error in errors))

    def test_missing_columns_are_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.csv"
            path.write_text("candidate_id,filename\n0001,coconut.jpg\n", encoding="utf-8")
            errors = validate(path)
        self.assertTrue(any("missing required columns" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

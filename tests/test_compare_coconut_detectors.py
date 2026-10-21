import csv
import tempfile
import unittest
from pathlib import Path

from tools.compare_coconut_detectors import compare_candidates, parse_candidate


class CompareCoconutDetectorsTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.truth = self.root / "truth.csv"
        self.good = self.root / "good.csv"
        self.bad = self.root / "bad.csv"
        self.write_csv(self.truth, [
            ["image_id", "xmin", "ymin", "xmax", "ymax", "class"],
            ["img1.jpg", "0", "0", "10", "10", "coconut"],
        ])
        self.write_csv(self.good, [
            ["image_id", "xmin", "ymin", "xmax", "ymax", "class", "score"],
            ["img1.jpg", "0", "0", "10", "10", "coconut", "0.95"],
        ])
        self.write_csv(self.bad, [
            ["image_id", "xmin", "ymin", "xmax", "ymax", "class", "score"],
            ["img1.jpg", "20", "20", "30", "30", "coconut", "0.90"],
        ])

    def tearDown(self):
        self.tempdir.cleanup()

    @staticmethod
    def write_csv(path, rows):
        with path.open("w", newline="", encoding="utf-8") as handle:
            csv.writer(handle).writerows(rows)

    def test_ranks_candidates_on_same_truth(self):
        report = compare_candidates(
            self.truth, [("weak", self.bad), ("strong", self.good)]
        )
        self.assertEqual(report["ground_truth_count"], 1)
        self.assertEqual(report["candidates"][0]["name"], "strong")
        self.assertEqual(report["candidates"][0]["f1"], 1.0)
        self.assertEqual(report["candidates"][0]["rank_by_detection_metrics"], 1)
        self.assertEqual(report["candidates"][1]["f1"], 0.0)

    def test_duplicate_candidate_names_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "unique"):
            compare_candidates(
                self.truth, [("same", self.good), ("same", self.bad)]
            )

    def test_empty_candidate_list_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "At least one"):
            compare_candidates(self.truth, [])

    def test_candidate_argument_requires_name_equals_path(self):
        with self.assertRaisesRegex(ValueError, "NAME=PATH"):
            parse_candidate("missing-separator")


if __name__ == "__main__":
    unittest.main()

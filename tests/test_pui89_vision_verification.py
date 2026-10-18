import unittest
from dataclasses import asdict

from pui89_vision.adapters import make_screening_record, verify_screening_record


class VerificationTests(unittest.TestCase):
    def test_record_is_review_only_and_verifies(self):
        record = make_screening_record("test-model", 0.8)
        self.assertEqual(record.status, "REVIEW_FLAG")
        self.assertTrue(record.human_review_required)
        self.assertFalse(record.actuator_authorized)
        self.assertTrue(verify_screening_record(record))

    def test_missing_score_abstains(self):
        record = make_screening_record("test-model", None)
        self.assertEqual(record.status, "ABSTAIN")
        self.assertTrue(verify_screening_record(record))

    def test_tampering_fails_verification(self):
        record = asdict(make_screening_record("test-model", 0.2))
        record["actuator_authorized"] = True
        self.assertFalse(verify_screening_record(record))

    def test_invalid_scores_rejected(self):
        for score in (-0.1, 1.1, float("nan"), float("inf")):
            with self.subTest(score=score):
                with self.assertRaises(ValueError):
                    make_screening_record("test-model", score)


if __name__ == "__main__":
    unittest.main()

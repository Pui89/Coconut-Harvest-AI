import unittest
from tools.pui89_world_state import Observation, assess_observation

class BoolNumericRegressionTests(unittest.TestCase):
    def test_bool_now_rejected(self):
        with self.assertRaises(ValueError):
            assess_observation(Observation("x", "s", 1.0, 0.9), now=True)
    def test_bool_max_age_rejected(self):
        with self.assertRaises(ValueError):
            assess_observation(Observation("x", "s", 1.0, 0.9), now=2.0, max_age_seconds=True)
    def test_bool_min_confidence_rejected(self):
        with self.assertRaises(ValueError):
            assess_observation(Observation("x", "s", 1.0, 0.9), now=2.0, min_confidence=False)
    def test_bool_timestamp_rejected(self):
        result = assess_observation(Observation("x", "s", True, 0.9), now=2.0)
        self.assertEqual(result.status, "REJECT")
    def test_bool_confidence_rejected(self):
        result = assess_observation(Observation("x", "s", 1.0, True), now=2.0)
        self.assertEqual(result.status, "REJECT")

if __name__ == "__main__":
    unittest.main()

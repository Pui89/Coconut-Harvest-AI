"""Standard-library tests for the PUI89 Pitfall Detector."""
import unittest

from pui89_core.pitfall_detector import inspect_state


class PitfallDetectorTests(unittest.TestCase):
    def test_clean_state_passes_configured_checks(self):
        report = inspect_state({"project": "test", "confidence": 0.95, "action": "inspect"})
        self.assertEqual(report["decision"], "PASS")
        self.assertFalse(report["findings"])

    def test_low_confidence_blocks(self):
        report = inspect_state({"confidence": 0.42})
        self.assertEqual(report["decision"], "BLOCK")
        self.assertIn("LOW_CONFIDENCE", {f["code"] for f in report["findings"]})

    def test_missing_required_field_blocks(self):
        report = inspect_state({"required_fields": ["depth_m"], "depth_m": None})
        self.assertEqual(report["decision"], "BLOCK")
        self.assertIn("MISSING_DATA", {f["code"] for f in report["findings"]})

    def test_sensor_conflict_blocks(self):
        report = inspect_state({"sensor_conflict": True})
        self.assertEqual(report["decision"], "BLOCK")
        self.assertIn("SENSOR_CONFLICT", {f["code"] for f in report["findings"]})

    def test_blockers_are_reported(self):
        report = inspect_state({"blockers": ["route is obstructed"]})
        self.assertEqual(report["decision"], "BLOCK")
        self.assertIn("SAFETY_BLOCKER", {f["code"] for f in report["findings"]})

    def test_medium_confidence_warns(self):
        report = inspect_state({"confidence": 0.72})
        self.assertEqual(report["decision"], "WARN")
        self.assertIn("UNCERTAIN_RESULT", {f["code"] for f in report["findings"]})


if __name__ == "__main__":
    unittest.main()

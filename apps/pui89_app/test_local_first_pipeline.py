"""No-download unit tests for the local-first proposal pipeline."""
import math
import tempfile
import unittest
from pathlib import Path

try:
    import numpy as np
except ImportError:
    np = None

from apps.pui89_app.local_first_pipeline import (
    Detection, Intrinsics, build_review_report, load_intrinsics,
    load_local_detector, localize_detection,
)

class LocalFirstPipelineTests(unittest.TestCase):
    def setUp(self):
        self.detection = Detection("coconut-001", 0.92, (40, 40, 60, 60))
        self.intrinsics = Intrinsics(100, 100, 50, 50)

    def test_missing_weights_fail_without_download(self):
        with self.assertRaises(FileNotFoundError):
            load_local_detector("definitely-not-present-coconut-model.pt")

    def test_human_review_never_authorizes_actuators(self):
        report = build_review_report([self.detection], {
            "coconut-001":{"status":"ESTIMATED_CAMERA_FRAME","x_m":0,"y_m":0,"z_m":1}
        }, human_approved_target="coconut-001")
        self.assertEqual(report["candidates"][0]["status"], "HUMAN_APPROVED_PROPOSAL_ONLY")
        self.assertFalse(report["actuator_commands_authorized"])
        self.assertEqual(report["robot_execution"], "NOT_IMPLEMENTED")

    def test_missing_depth_rejects_candidate(self):
        report = build_review_report([self.detection], {})
        self.assertEqual(report["candidates"][0]["status"], "REJECTED")
        self.assertIn("3D location unavailable or invalid", report["candidates"][0]["reasons"])

    def test_low_confidence_rejected(self):
        low = Detection("low", 0.2, (1, 1, 2, 2))
        report = build_review_report([low], {})
        self.assertIn("confidence below configured threshold", report["candidates"][0]["reasons"])

    def test_nonfinite_threshold_rejected(self):
        with self.assertRaises(ValueError):
            build_review_report([], {}, min_confidence=math.nan)

    def test_unordered_range_rejected(self):
        with self.assertRaises(ValueError):
            build_review_report([], {}, min_range_m=3, max_range_m=1)

    def test_non_coconut_class_not_constructed_by_report(self):
        other = Detection("other", 0.99, (1, 1, 2, 2), class_name="person")
        report = build_review_report([other], {})
        self.assertEqual(report["candidates"][0]["target_id"], "other")
        self.assertFalse(report["actuator_commands_authorized"])

    def test_intrinsics_validate_focal_length(self):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder) / "camera.json"
            p.write_text('{"fx":0,"fy":100,"cx":50,"cy":50}', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_intrinsics(p)

    @unittest.skipIf(np is None, "NumPy not installed")
    def test_median_depth_localization(self):
        depth = np.full((100, 100), 2.0)
        depth[48:53, 48:53] = 1.5
        result = localize_detection(self.detection, depth, self.intrinsics)
        self.assertEqual(result["status"], "ESTIMATED_CAMERA_FRAME")
        self.assertAlmostEqual(result["x_m"], 0.0)
        self.assertAlmostEqual(result["y_m"], 0.0)
        self.assertAlmostEqual(result["z_m"], 1.5)

    @unittest.skipIf(np is None, "NumPy not installed")
    def test_invalid_depth_is_unknown(self):
        result = localize_detection(self.detection, np.zeros((100, 100)), self.intrinsics)
        self.assertEqual(result["status"], "UNKNOWN")

if __name__ == "__main__":
    unittest.main()

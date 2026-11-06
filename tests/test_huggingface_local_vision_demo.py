import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "huggingface_local_vision_demo.py"
SPEC = importlib.util.spec_from_file_location("pui89_hf_demo", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class HuggingFaceLocalVisionDemoTests(unittest.TestCase):
    def test_report_is_review_only_and_non_actuating(self):
        report = MODULE.build_report(
            image_path="fixture.jpg", image_sha256="abc", model_id=MODULE.MODEL_ID,
            revision="test-revision", labels=["person"], threshold=0.2,
            detections=[{"label": "person", "score": 0.7, "box_xyxy": [1, 2, 3, 4]}]
        )
        self.assertEqual(report["status"], "MODEL_INFERENCE_REVIEW_ONLY")
        self.assertTrue(report["human_review_required"])
        self.assertFalse(report["actuator_authorized"])
        self.assertEqual(report["model"]["id"], "google/owlvit-base-patch32")

    def test_invalid_threshold_rejected(self):
        with self.assertRaises(ValueError):
            MODULE.build_report(
                image_path="fixture.jpg", image_sha256="abc", model_id=MODULE.MODEL_ID,
                revision="test-revision", labels=["person"], threshold=1.1, detections=[]
            )

    def test_project_scope_and_labels_are_recorded(self):
        report = MODULE.build_report(
            image_path="fixture.jpg", image_sha256="abc", model_id=MODULE.MODEL_ID,
            revision="test-revision", labels=MODULE.DEFAULT_LABELS, threshold=0.2, detections=[]
        )
        self.assertEqual(report["candidate_labels"], MODULE.DEFAULT_LABELS)
        self.assertTrue(report["scope"])


if __name__ == "__main__":
    unittest.main()

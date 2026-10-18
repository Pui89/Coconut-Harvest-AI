"""Mocked, no-download integration test from local detector output to robot simulation."""
import tempfile
import unittest
from pathlib import Path

import numpy as np

from apps.pui89_app.local_first_pipeline import (
    Intrinsics, build_review_report, localize_detection, run_local_detector,
)
from apps.pui89_app.vision_to_workflow import run_vision_to_simulated_workflow


class Scalar:
    def __init__(self, value):
        self.value = value
    def item(self):
        return self.value


class Row:
    def __init__(self, values):
        self.values = values
    def tolist(self):
        return self.values


class Box:
    def __init__(self, class_id, confidence, xyxy):
        self.cls = Scalar(class_id)
        self.conf = Scalar(confidence)
        self.xyxy = [Row(xyxy)]


class FakeModel:
    names = {0: "coconut", 1: "person"}
    def predict(self, **kwargs):
        return [type("Result", (), {
            "names": self.names,
            "boxes": [
                Box(0, 0.95, [40, 40, 60, 60]),
                Box(1, 0.99, [10, 10, 20, 20]),
            ],
        })()]


class LocalToSimulationIntegrationTests(unittest.TestCase):
    def test_mock_detector_rgbd_and_robot_simulation_path(self):
        with tempfile.TemporaryDirectory() as folder:
            image = Path(folder) / "orchard.jpg"
            image.write_bytes(b"fake-image-for-mocked-detector")
            detections = run_local_detector(FakeModel(), image)
        self.assertEqual(len(detections), 1)
        self.assertEqual(detections[0].class_name, "coconut")

        depth = np.full((100, 100), 1.5, dtype=float)
        localization = localize_detection(
            detections[0], depth, Intrinsics(fx=100, fy=100, cx=50, cy=50)
        )
        proposal = build_review_report(
            detections, {detections[0].target_id: localization}
        )
        evidence = {
            "now_s": 10.0,
            "camera_to_robot_base_4x4": [
                [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]
            ],
            "evidence_by_target": {
                detections[0].target_id: {
                    "localization_uncertainty_m": 0.03,
                    "track_age_frames": 8,
                    "timestamp_s": 9.9,
                    "obstacle_clearance_m": 0.5,
                    "reachable": True,
                }
            },
        }
        waiting = run_vision_to_simulated_workflow(proposal, evidence)
        self.assertEqual(waiting["workflow_report"]["status"], "AWAITING_HUMAN_APPROVAL")
        completed = run_vision_to_simulated_workflow(
            proposal, evidence, human_approved=True
        )
        report = completed["workflow_report"]
        self.assertEqual(report["status"], "COMPLETED_SIMULATION")
        self.assertEqual(len(report["plan"]), 3)
        self.assertFalse(completed["actuator_commands_sent"])
        self.assertFalse(completed["physical_harvest_verified"])


if __name__ == "__main__":
    unittest.main()

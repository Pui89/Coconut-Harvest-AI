import math
import unittest

from apps.pui89_app.vision_to_workflow import (
    proposal_to_candidates,
    run_vision_to_simulated_workflow,
    transform_camera_point,
)

IDENTITY = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
PROPOSAL = {
    "mode": "LOCAL_ONLY_PROPOSAL",
    "actuator_commands_authorized": False,
    "candidates": [{
        "target_id": "coconut-001", "confidence": 0.92,
        "box_xyxy": [40,40,60,60], "status": "REVIEW_REQUIRED",
        "localization": {"status": "ESTIMATED_CAMERA_FRAME", "x_m": 0.5, "y_m": 0.2, "z_m": 1.0},
        "reasons": [],
    }],
}
EVIDENCE = {
    "now_s": 10.0,
    "camera_to_robot_base_4x4": IDENTITY,
    "evidence_by_target": {
        "coconut-001": {
            "localization_uncertainty_m": 0.03,
            "track_age_frames": 8, "timestamp_s": 9.9,
            "obstacle_clearance_m": 0.5, "reachable": True,
        }
    },
}

class VisionToWorkflowTests(unittest.TestCase):
    def test_transform_point_uses_explicit_translation(self):
        matrix = [[1,0,0,1],[0,1,0,2],[0,0,1,3],[0,0,0,1]]
        self.assertEqual(transform_camera_point((1,2,3), matrix), (2.0,4.0,6.0))

    def test_complete_evidence_reaches_simulation_only_plan(self):
        result = run_vision_to_simulated_workflow(PROPOSAL, EVIDENCE, human_approved=True)
        report = result["workflow_report"]
        self.assertEqual(report["selected_target_id"], "coconut-001")
        self.assertEqual(report["status"], "COMPLETED_SIMULATION")
        self.assertFalse(result["actuator_commands_sent"])
        self.assertFalse(result["physical_harvest_verified"])

    def test_missing_transform_fails_closed(self):
        evidence = dict(EVIDENCE)
        evidence.pop("camera_to_robot_base_4x4")
        candidates, _ = proposal_to_candidates(PROPOSAL, evidence)
        self.assertIsNone(candidates[0].world_position_m)
        result = run_vision_to_simulated_workflow(PROPOSAL, evidence, human_approved=True)
        self.assertIsNone(result["workflow_report"]["selected_target_id"])
        self.assertEqual(result["workflow_report"]["status"], "SAFE_HOLD")

    def test_missing_robot_evidence_fails_closed(self):
        evidence = {"now_s": 10.0, "camera_to_robot_base_4x4": IDENTITY, "evidence_by_target": {}}
        result = run_vision_to_simulated_workflow(PROPOSAL, evidence, human_approved=True)
        self.assertIsNone(result["workflow_report"]["selected_target_id"])
        self.assertEqual(result["workflow_report"]["status"], "SAFE_HOLD")

    def test_emergency_stop_forces_safe_hold(self):
        result = run_vision_to_simulated_workflow(PROPOSAL, EVIDENCE, emergency_stop=True)
        self.assertEqual(result["workflow_report"]["status"], "SAFE_HOLD")
        self.assertFalse(result["actuator_commands_sent"])

    def test_rejected_upstream_candidates_are_not_planned(self):
        proposal = dict(PROPOSAL)
        proposal["candidates"] = [dict(PROPOSAL["candidates"][0], status="REJECTED", reasons=["LOW_CONFIDENCE"])]
        result = run_vision_to_simulated_workflow(proposal, EVIDENCE, human_approved=True)
        self.assertEqual(result["upstream_rejected_candidates"]["coconut-001"], ["LOW_CONFIDENCE"])
        self.assertEqual(result["workflow_report"]["status"], "SAFE_HOLD")

    def test_bad_transform_is_rejected(self):
        evidence = dict(EVIDENCE)
        evidence["camera_to_robot_base_4x4"] = [[1,2],[3,4]]
        with self.assertRaises(ValueError):
            proposal_to_candidates(PROPOSAL, evidence)

    def test_non_rigid_transform_is_rejected(self):
        evidence = dict(EVIDENCE)
        evidence["camera_to_robot_base_4x4"] = [
            [2,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]
        ]
        with self.assertRaises(ValueError):
            proposal_to_candidates(PROPOSAL, evidence)

    def test_untrusted_proposal_mode_is_rejected(self):
        proposal = dict(PROPOSAL)
        proposal["mode"] = "SOME_OTHER_MODE"
        with self.assertRaises(ValueError):
            proposal_to_candidates(proposal, EVIDENCE)

    def test_actuator_authorization_in_proposal_is_rejected(self):
        proposal = dict(PROPOSAL)
        proposal["actuator_commands_authorized"] = True
        with self.assertRaises(ValueError):
            proposal_to_candidates(proposal, EVIDENCE)

if __name__ == "__main__":
    unittest.main()

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "ros2" / "pui89_sim_bridge"
sys.path.insert(0, str(BRIDGE))

from pui89_sim_bridge.decision_gate import evaluate_world_state  # noqa: E402


class DecisionGateTests(unittest.TestCase):
    def test_nominal_proposal_is_allowlisted_and_simulation_only(self):
        result = evaluate_world_state(
            {"sensors_ok": True, "comms_ok": True, "confidence": 0.95},
            ready_action="HARVEST_STEP_SIMULATION_ONLY",
        )
        self.assertEqual(result["action"], "HARVEST_STEP_SIMULATION_ONLY")
        self.assertFalse(result["hardware_actuation"])
        self.assertTrue(result["simulation_only"])

    def test_faults_force_safe_hold(self):
        for state in (
            {"emergency_stop": True},
            {"sensors_ok": False},
            {"sensor_data_fresh": False},
            {"comms_ok": False},
            {"battery_ok": False},
            {"propulsion_ok": False},
        ):
            with self.subTest(state=state):
                self.assertEqual(
                    evaluate_world_state(state, ready_action="PLAN_RESCUE_ROUTE_SIMULATION_ONLY")["action"],
                    "SAFE_HOLD",
                )

    def test_uncertainty_abstains(self):
        for state in (
            {"confidence": 0.1},
            {"confidence": float("nan")},
            {"confidence": "high"},
            {"modalities_conflict": True},
            {"missing_required_modality": True},
        ):
            with self.subTest(state=state):
                self.assertEqual(
                    evaluate_world_state(state, ready_action="REQUEST_HUMAN_REVIEW")["action"],
                    "UNKNOWN",
                )

    def test_target_missing_requests_search(self):
        self.assertEqual(
            evaluate_world_state(
                {"target_visible": False}, ready_action="HARVEST_STEP_SIMULATION_ONLY"
            )["action"],
            "SEARCH",
        )

    def test_human_review_takes_precedence(self):
        self.assertEqual(
            evaluate_world_state(
                {"human_review_required": True}, ready_action="PLAN_RESCUE_ROUTE_SIMULATION_ONLY"
            )["action"],
            "REQUEST_HUMAN_REVIEW",
        )

    def test_non_allowlisted_ready_action_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_world_state({"confidence": 0.9}, ready_action="MOVE_ROBOT_NOW")

    def test_bridge_uses_only_simulation_topics(self):
        node = (BRIDGE / "pui89_sim_bridge" / "proposal_node.py").read_text(encoding="utf-8")
        self.assertIn("/pui89/sim/world_state", node)
        self.assertIn("/pui89/sim/action_proposal", node)
        self.assertNotIn("cmd_vel", node)
        self.assertNotIn("mavlink", node.lower())

    def test_vlm_smoke_tool_is_local_only(self):
        script = (ROOT / "tools" / "smolvlm_local_smoke_test.py").read_text(encoding="utf-8")
        self.assertIn("local_files_only=True", script)
        self.assertIn("HF_HUB_OFFLINE", script)
        self.assertNotIn("snapshot_download", script)


if __name__ == "__main__":
    unittest.main()

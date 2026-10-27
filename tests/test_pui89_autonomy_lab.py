import json, sys, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from pui89_autonomy_lab import MockVLA, model_preflight, run_scenarios  # noqa: E402

class MockVLAGuardTests(unittest.TestCase):
    def setUp(self): self.policy = MockVLA(0.65)
    def test_estop_sensor_stale_comms_hold(self):
        for state in ({"emergency_stop": True},{"sensors_ok": False},{"sensor_data_fresh": False},{"comms_ok": False}):
            with self.subTest(state=state): self.assertEqual(self.policy.propose(state,"SIM_ACTION")[0],"SAFE_HOLD")
    def test_malformed_safety_flags_fail_safe(self):
        for state in ({"sensors_ok": "false"}, {"comms_ok": 1},
                      {"operator_approved": "yes"}, {"target_visible": 0},
                      {"human_review_required": None}):
            with self.subTest(state=state):
                self.assertEqual(self.policy.propose(state, "SIM_ACTION")[0], "SAFE_HOLD")

    def test_boolean_confidence_is_not_numeric(self):
        for value in (True, False):
            with self.subTest(value=value):
                self.assertEqual(self.policy.propose({"confidence": value}, "SIM_ACTION")[0], "UNKNOWN")

    def test_invalid_confidence_threshold_rejected(self):
        for value in (True, -0.1, 1.1, float("nan"), float("inf"), "0.65"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    MockVLA(value)

    def test_scenario_config_does_not_coerce_invalid_threshold(self):
        invalid_values = (True, "0.65", None, -0.1, 1.1)
        for value in invalid_values:
            with self.subTest(value=value), tempfile.TemporaryDirectory() as tmp:
                config = {
                    "schema_version": 1,
                    "project_id": "threshold-validation-test",
                    "confidence_threshold": value,
                    "scenarios": [{"id": "one", "steps": [
                        {"state": {}, "expected_action": "SIM_ACTION", "dt_s": 1.0}
                    ]}],
                }
                config_path = Path(tmp) / "scenario.json"
                config_path.write_text(json.dumps(config), encoding="utf-8")
                with self.assertRaises(ValueError):
                    run_scenarios(config_path, Path(tmp) / "out")

    def test_low_confidence_or_conflicting_modalities_abstain(self):
        for state in ({"confidence":0.2},{"modalities_conflict":True},{"missing_required_modality":True},{"confidence":2.0},{"confidence":None},{"confidence":"not-a-number"},{"confidence":float("nan")},{"confidence":float("inf")}):
            with self.subTest(state=state): self.assertEqual(self.policy.propose(state,"SIM_ACTION")[0],"UNKNOWN")
    def test_missing_target_searches(self):
        self.assertEqual(self.policy.propose({"target_visible":False},"SIM_ACTION")[0],"SEARCH")
    def test_human_review_blocks_nominal_action(self):
        self.assertEqual(self.policy.propose({"human_review_required":True},"ENFORCEMENT_ACTION")[0],"REQUEST_HUMAN_REVIEW")
    def test_simulation_has_stable_id_and_never_actuates(self):
        with tempfile.TemporaryDirectory() as tmp:
            report=run_scenarios(ROOT/"simulation/scenarios.json",Path(tmp))
            self.assertEqual(report["metrics"]["failure_count"],0)
            again=run_scenarios(ROOT/"simulation/scenarios.json",Path(tmp))
            self.assertEqual(report["run_id"],again["run_id"])
            self.assertTrue(all(not row["hardware_actuation"] for row in report["steps"]))
            saved=json.loads(Path(report["output_files"]["json"]).read_text(encoding="utf-8"))
            self.assertEqual(saved["run_id"],report["run_id"])
    def test_model_preflight_never_downloads(self):
        with tempfile.TemporaryDirectory() as tmp: report=model_preflight(Path(tmp))
        self.assertFalse(report["download_performed"]); self.assertFalse(report["software_installed"])
        self.assertFalse(report["hardware_actuation"])
        self.assertEqual(report["model_id"],"HuggingFaceTB/SmolVLM-256M-Instruct")


    def test_world_state_persists_and_recovers(self):
        config = {
            "schema_version": 1,
            "project_id": "world-state-test",
            "action_if_ready": "CONTINUE_SIMULATION_ONLY",
            "scenarios": [{
                "id": "fault-and-recovery",
                "seed": 42,
                "steps": [
                    {"state": {"sensors_ok": True, "sensor_data_fresh": True, "confidence": 0.9},
                     "expected_action": "CONTINUE_SIMULATION_ONLY"},
                    {"state": {"sensor_data_fresh": False},
                     "expected_action": "SAFE_HOLD"},
                    {"state": {"sensor_data_fresh": True},
                     "expected_action": "CONTINUE_SIMULATION_ONLY"}
                ]
            }]
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config_path = root / "scenarios.json"
            config_path.write_text(json.dumps(config), encoding="utf-8")
            report = run_scenarios(config_path, root / "reports")
        self.assertEqual(report["metrics"]["failure_count"], 0)
        self.assertTrue(report["steps"][1]["state"]["sensors_ok"])
        self.assertFalse(report["steps"][1]["state"]["sensor_data_fresh"])
        self.assertTrue(report["steps"][2]["state"]["sensor_data_fresh"])

if __name__ == "__main__": unittest.main()

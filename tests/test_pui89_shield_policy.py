"""Standard-library regression tests for the PUI89 SHIELD reference policy."""
import json
import unittest
from pathlib import Path

from pui89_shield_policy import (
    HazardAssessment,
    WarningState,
    classify_warning,
    proposal_requires_human_review,
)


ROOT = Path(__file__).resolve().parents[1]


class ShieldWarningPolicyTests(unittest.TestCase):
    def test_valid_low_risk_evidence_is_normal(self):
        self.assertEqual(classify_warning(HazardAssessment(
            observation_valid=True, severity="low", evidence_refs=("ev-001",)
        )), WarningState.NORMAL)

    def test_advisory_is_preserved(self):
        self.assertEqual(classify_warning(HazardAssessment(
            observation_valid=True, advisory=True, evidence_refs=("ev-002",)
        )), WarningState.ADVISORY)

    def test_high_severity_is_warning(self):
        self.assertEqual(classify_warning(HazardAssessment(
            observation_valid=True, severity="high", evidence_refs=("ev-003",)
        )), WarningState.WARNING)

    def test_critical_severity_is_critical(self):
        self.assertEqual(classify_warning(HazardAssessment(
            observation_valid=True, severity="critical", evidence_refs=("ev-004",)
        )), WarningState.CRITICAL)

    def test_missing_observation_fails_degraded_not_normal(self):
        self.assertEqual(classify_warning(HazardAssessment(
            observation_valid=False
        )), WarningState.UNKNOWN_DEGRADED)

    def test_conflicting_sensors_fail_degraded(self):
        self.assertEqual(classify_warning(HazardAssessment(
            observation_valid=True, sensor_conflict=True
        )), WarningState.UNKNOWN_DEGRADED)

    def test_unsubstantiated_hazard_fails_degraded(self):
        self.assertEqual(classify_warning(HazardAssessment(
            observation_valid=True, severity="critical"
        )), WarningState.UNKNOWN_DEGRADED)

    def test_confirmed_imminent_hazard_requires_evidence(self):
        self.assertEqual(classify_warning(HazardAssessment(
            observation_valid=True, imminent_hazard_confirmed=True
        )), WarningState.UNKNOWN_DEGRADED)

    def test_confirmed_imminent_hazard_with_evidence_is_emergency(self):
        self.assertEqual(classify_warning(HazardAssessment(
            observation_valid=True, imminent_hazard_confirmed=True,
            evidence_refs=("ev-009",)
        )), WarningState.EMERGENCY)

    def test_physical_action_proposal_requires_human_review(self):
        self.assertTrue(proposal_requires_human_review(physical_action=True))

    def test_nonphysical_report_does_not_claim_actuation_authority(self):
        self.assertFalse(proposal_requires_human_review(physical_action=False))


class ShieldContractTests(unittest.TestCase):
    def test_event_schema_has_required_contract_fields(self):
        schema_path = ROOT / "schemas/pui89-shield-event.schema.json"
        if not schema_path.is_file():
            schema_path = ROOT / "schemas/pui89-shield-warning-event-v1.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        required = set(schema["required"])
        expected = {
            "event_id", "schema_version", "project", "component", "observed_at",
            "source_id", "value", "unit", "quality", "evidence_refs",
            "uncertainty", "hazard", "severity", "warning_state", "decision",
            "rationale", "human_approval_required", "software_version"
        }
        self.assertTrue(expected.issubset(required))

    def test_profile_keeps_physical_validation_unverified(self):
        profile = json.loads((ROOT / ".github/pui89-resilience.json").read_text(encoding="utf-8"))
        self.assertEqual(profile["shield_system"]["physical_validation"], "NOT_VERIFIED")
        self.assertEqual(len(profile["shield_system"]["warning_states"]), 6)

    def test_scenario_catalog_is_explicitly_not_test_evidence(self):
        catalog = json.loads((ROOT / "docs/PUI89_SHIELD_TEST_SCENARIOS.json").read_text(encoding="utf-8"))
        self.assertEqual(catalog["status"], "scenario_catalog_only_not_simulation_evidence")
        self.assertGreaterEqual(len(catalog["scenarios"]), 10)


if __name__ == "__main__":
    unittest.main()

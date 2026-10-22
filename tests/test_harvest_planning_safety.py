from __future__ import annotations

import unittest

from agents.harvest_planning_agent import (
    AgentConfig,
    CoconutCandidate,
    assess_candidate,
    propose_plan,
)


class HarvestPlanningSafetyTests(unittest.TestCase):
    def candidate(self, **overrides):
        values = {
            "target_id": "test-coconut",
            "confidence": 0.9,
            "x_m": 1.0,
            "y_m": 0.0,
            "z_m": 1.0,
            "reachable": True,
            "occluded": False,
            "stage": "mature_green",
        }
        values.update(overrides)
        return CoconutCandidate(**values)

    def test_missing_3d_position_is_rejected_by_default(self):
        result = assess_candidate(self.candidate(x_m=None))
        self.assertEqual(result.status, "REJECTED")
        self.assertTrue(any("3D position missing" in reason for reason in result.reasons))

    def test_unconfirmed_reachability_is_rejected(self):
        result = assess_candidate(self.candidate(reachable=None))
        self.assertEqual(result.status, "REJECTED")
        self.assertTrue(any("reachability has not been confirmed" in reason for reason in result.reasons))

    def test_invalid_confidence_is_rejected(self):
        for confidence in (-0.1, 1.1, float("nan")):
            with self.subTest(confidence=confidence):
                result = assess_candidate(self.candidate(confidence=confidence))
                self.assertEqual(result.status, "REJECTED")

    def test_infinite_confidence_is_rejected(self):
        result = assess_candidate(self.candidate(confidence=float("inf")))
        self.assertEqual(result.status, "REJECTED")
        self.assertTrue(any("confidence must be between 0 and 1" in reason for reason in result.reasons))

    def test_non_finite_3d_position_is_rejected(self):
        for field, value in (("x_m", float("nan")), ("y_m", float("inf")), ("z_m", float("-inf"))):
            with self.subTest(field=field):
                result = assess_candidate(self.candidate(**{field: value}))
                self.assertEqual(result.status, "REJECTED")
                self.assertIsNone(result.distance_m)
                self.assertTrue(any("non-finite" in reason for reason in result.reasons))

    def test_occluded_target_is_rejected(self):
        result = assess_candidate(self.candidate(occluded=True))
        self.assertEqual(result.status, "REJECTED")
        self.assertTrue(any("occluded" in reason for reason in result.reasons))

    def test_stage_filter_rejects_wrong_maturity_stage(self):
        result = assess_candidate(
            self.candidate(stage="young_green"),
            selected_stages={"mature_green"},
        )
        self.assertEqual(result.status, "REJECTED")

    def test_survey_only_never_marks_target_eligible(self):
        result = propose_plan([self.candidate()], harvest_mode="survey_only")
        self.assertEqual(result["status"], "SAFE_HOLD")
        self.assertEqual(result["eligible_target_ids"], [])
        self.assertFalse(result["safety_boundary"]["actuator_commands_sent"])
        self.assertFalse(result["safety_boundary"]["physical_robot_authorized"])

    def test_selected_combination_cannot_enable_uncertain_stage(self):
        with self.assertRaises(ValueError):
            propose_plan(
                [self.candidate(stage="uncertain_stage")],
                harvest_mode="selected_combination",
                selected_stages=["uncertain_stage"],
            )

    def test_range_limit_is_configurable_and_enforced(self):
        result = assess_candidate(
            self.candidate(x_m=2.0, y_m=0.0, z_m=0.0),
            config=AgentConfig(max_range_m=1.0),
        )
        self.assertEqual(result.status, "REJECTED")
        self.assertTrue(any("outside configured range" in reason for reason in result.reasons))


if __name__ == "__main__":
    unittest.main()

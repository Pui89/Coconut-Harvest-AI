"""Tests for model-agnostic VLM/Action-LLM contracts; no model or network required."""
import unittest

from pui89_autonomy.llm_interfaces import (
    ActionPlan,
    ActionStep,
    VisionFinding,
    validate_action_plan,
    validate_vision_finding,
)


class VisionFindingTests(unittest.TestCase):
    def test_valid_finding(self):
        item = VisionFinding("mature_coconut", 0.92, "image-001", (0.1, 0.2, 0.5, 0.8))
        self.assertEqual(validate_vision_finding(item), ())

    def test_rejects_invalid_confidence_and_box(self):
        item = VisionFinding("object", float("nan"), "image-001", (0.8, 0.2, 0.1, 0.9))
        issues = validate_vision_finding(item)
        self.assertTrue(any("confidence" in issue for issue in issues))
        self.assertTrue(any("bbox_xyxy" in issue for issue in issues))

    def test_requires_provenance(self):
        item = VisionFinding("person", 0.8, " ")
        self.assertIn("source_id/provenance must not be empty", validate_vision_finding(item))


class ActionPlanTests(unittest.TestCase):
    def test_accepts_allowlisted_plan_but_does_not_execute_it(self):
        plan = ActionPlan("inspect target", (ActionStep("inspect", {"zone": "A"}),))
        self.assertEqual(validate_action_plan(plan, ["inspect"]), ())

    def test_rejects_unknown_action(self):
        plan = ActionPlan("inspect target", (ActionStep("unlock_door"),))
        self.assertTrue(any("not allowlisted" in issue for issue in validate_action_plan(plan, ["inspect"])))

    def test_rejects_human_review_disabled(self):
        plan = ActionPlan("inspect target", (ActionStep("inspect"),), requires_human_review=False)
        self.assertTrue(any("human review" in issue for issue in validate_action_plan(plan, ["inspect"])))

    def test_rejects_nonfinite_parameters(self):
        plan = ActionPlan("inspect target", (ActionStep("inspect", {"score": float("inf")}),))
        self.assertTrue(any("finite JSON-like" in issue for issue in validate_action_plan(plan, ["inspect"])))

    def test_rejects_empty_plan(self):
        plan = ActionPlan("inspect target", ())
        self.assertTrue(any("at least one step" in issue for issue in validate_action_plan(plan, ["inspect"])))


if __name__ == "__main__":
    unittest.main()

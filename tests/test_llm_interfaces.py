"""Tests for model-agnostic vision and action-plan contracts; no model/network required."""
import unittest

from pui89_autonomy.llm_interfaces import (
    ActionPlan, ActionStep, VisionFinding,
    validate_action_plan, validate_vision_finding,
)


class VisionFindingTests(unittest.TestCase):
    def test_valid_finding_and_boundary_confidence(self):
        for confidence in (0.0, 1.0, 0.92):
            item = VisionFinding("mature_coconut", confidence, "image-001", (0.1, 0.2, 0.5, 0.8))
            self.assertEqual(validate_vision_finding(item), ())

    def test_rejects_invalid_confidence_and_box(self):
        item = VisionFinding("object", float("nan"), "image-001", (0.8, 0.2, 0.1, 0.9))
        issues = validate_vision_finding(item)
        self.assertTrue(any("confidence" in issue for issue in issues))
        self.assertTrue(any("bbox_xyxy" in issue for issue in issues))

    def test_rejects_non_numeric_and_boolean_confidence_without_crashing(self):
        for value in ("high", None, True, float("inf"), -0.1, 1.1):
            with self.subTest(value=value):
                self.assertTrue(validate_vision_finding(VisionFinding("person", value, "src")))

    def test_requires_label_and_provenance(self):
        self.assertTrue(validate_vision_finding(VisionFinding("", 0.8, " ")))

    def test_rejects_non_numeric_bbox_values_without_crashing(self):
        item = VisionFinding("person", 0.8, "src", (0.1, "bad", 0.8, 0.9))
        self.assertTrue(any("bbox_xyxy" in issue for issue in validate_vision_finding(item)))

    def test_rejects_zero_area_or_out_of_range_bbox(self):
        for box in ((0.2, 0.2, 0.2, 0.8), (-0.1, 0.2, 0.5, 0.8), (0.1, 0.2, 1.1, 0.8)):
            with self.subTest(box=box):
                self.assertTrue(any("bbox_xyxy" in issue for issue in validate_vision_finding(
                    VisionFinding("object", 0.8, "src", box)
                )))


class ActionPlanTests(unittest.TestCase):
    def test_accepts_allowlisted_plan_but_does_not_execute_it(self):
        plan = ActionPlan("inspect target", (ActionStep("inspect", {"zone": "A"}),))
        self.assertEqual(validate_action_plan(plan, ["inspect"]), ())

    def test_rejects_unknown_action_and_human_review_disabled(self):
        plan = ActionPlan("inspect target", (ActionStep("unlock_door"),), requires_human_review=False)
        issues = validate_action_plan(plan, ["inspect"])
        self.assertTrue(any("not allowlisted" in issue for issue in issues))
        self.assertTrue(any("human review" in issue for issue in issues))

    def test_rejects_nonfinite_nested_parameters(self):
        plan = ActionPlan("inspect target", (ActionStep("inspect", {"nested": [1, {"score": float("inf")}]}),))
        self.assertTrue(any("finite JSON-like" in issue for issue in validate_action_plan(plan, ["inspect"])))

    def test_rejects_empty_plan_and_blank_goal(self):
        self.assertTrue(validate_action_plan(ActionPlan("", ()), ["inspect"]))

    def test_rejects_plan_over_step_limit(self):
        plan = ActionPlan("inspect", (ActionStep("inspect"), ActionStep("inspect")))
        self.assertTrue(any("no more than 1" in issue for issue in validate_action_plan(plan, ["inspect"], max_steps=1)))

    def test_rejects_invalid_step_limit(self):
        plan = ActionPlan("inspect", (ActionStep("inspect"),))
        for limit in (0, -1, True, 1.5):
            with self.subTest(limit=limit):
                self.assertTrue(any("max_steps" in issue for issue in validate_action_plan(plan, ["inspect"], max_steps=limit)))

    def test_rejects_arbitrary_step_objects(self):
        plan = ActionPlan("inspect", ("run arbitrary code",))
        self.assertTrue(any("ActionStep" in issue for issue in validate_action_plan(plan, ["inspect"])))


if __name__ == "__main__":
    unittest.main()

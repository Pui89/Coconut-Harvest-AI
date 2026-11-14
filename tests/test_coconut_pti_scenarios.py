"""Synthetic adverse-condition scenarios for the Coconut PTI adapter.

These tests do not simulate image processing. They verify conservative handling
when the caller supplies uncertain, degraded, stale, or conflicting findings.
"""
import unittest

from pui89_autonomy.llm_interfaces import VisionFinding
from tools.pui89_coconut_pti_adapter import build_coconut_pti_packet

CURRENT_TS = "2026-11-14T14:00:00+07:00"
OLD_TS = "2025-01-01T08:00:00+07:00"


def packet(label, confidence, *, timestamp=CURRENT_TS, source="synthetic-frame"):
    return build_coconut_pti_packet(
        VisionFinding(label, confidence, source, (0.1, 0.2, 0.6, 0.8)),
        observation_id=f"obs-{source}",
        state_id=f"state-{source}",
        proposal_id=f"proposal-{source}",
        timestamp=timestamp,
        frame_id=source,
    )


class CoconutPtiScenarioTests(unittest.TestCase):
    def assert_review_only(self, result):
        self.assertEqual(result["status"], "HUMAN_REVIEW_REQUIRED")
        self.assertFalse(result["execution_authorized"])
        self.assertFalse(result["physical_actuation_authorized"])
        self.assertTrue(result["action_proposal"]["human_approval_required"])
        self.assertFalse(result["action_proposal"]["actuation_allowed"])
        self.assertEqual(result["action_proposal"]["authority"], "advisory_only")

    def test_low_light_or_blur_cannot_be_claimed_as_quality_checked(self):
        # The current adapter receives no image-quality assessment input.
        # Therefore degraded-image conditions must remain explicitly unknown.
        result = packet("mature_green", 0.54, source="low-light-blurred-frame")
        self.assertEqual(result["observation"]["quality"], "unknown")
        self.assertEqual(result["observation"]["integrity_status"], "unverified")
        self.assert_review_only(result)

    def test_occlusion_does_not_turn_candidate_into_verified_maturity(self):
        result = packet("yellow", 0.62, source="partially-occluded-frame")
        self.assertEqual(
            result["world_state"]["state"]["visual_maturity_candidate"], "yellow"
        )
        self.assertEqual(result["world_state"]["uncertainty"]["level"], "unknown")
        self.assertEqual(result["world_state"]["state"]["harvestability"], "not_assessed")
        self.assert_review_only(result)

    def test_stale_timestamp_is_not_silently_marked_fresh(self):
        result = packet("brown", 0.88, timestamp=OLD_TS, source="old-frame")
        self.assertEqual(result["world_state"]["freshness"], "unknown")
        self.assertEqual(result["observation"]["timestamp"], OLD_TS)
        self.assert_review_only(result)

    def test_conflicting_findings_are_not_automatically_fused(self):
        first = packet("young_green", 0.93, source="camera-a")
        second = packet("brown", 0.89, source="camera-b")
        self.assertNotEqual(
            first["world_state"]["state"]["visual_maturity_candidate"],
            second["world_state"]["state"]["visual_maturity_candidate"],
        )
        # Separate packets remain separate evidence; no winner is selected.
        self.assertEqual(first["world_state"]["observation_refs"], ["obs-camera-a"])
        self.assertEqual(second["world_state"]["observation_refs"], ["obs-camera-b"])
        self.assert_review_only(first)
        self.assert_review_only(second)

    def test_unknown_label_and_unverified_provenance_stay_unknown(self):
        result = packet("possibly_mature", 0.99, source="unverified-source")
        self.assertEqual(
            result["world_state"]["state"]["visual_maturity_candidate"], "unknown"
        )
        self.assertEqual(
            result["observation"]["provenance"]["rights_status"], "unknown"
        )
        self.assertEqual(result["observation"]["integrity_status"], "unverified")
        self.assert_review_only(result)

    def test_no_scenario_claims_height_or_harvestability(self):
        for source in ("low-light", "blur", "occlusion", "stale", "conflict"):
            with self.subTest(source=source):
                result = packet("mature_green", 0.95, source=source)
                state = result["world_state"]["state"]
                self.assertIsNone(state["height_m"])
                self.assertEqual(state["height_status"], "unverified")
                self.assertEqual(state["harvestability"], "not_assessed")
                self.assert_review_only(result)


if __name__ == "__main__":
    unittest.main()

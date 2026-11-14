"""Synthetic tests for the Coconut PTI shared-contract adapter."""
import unittest

from pui89_autonomy.llm_interfaces import VisionFinding
from tools.pui89_coconut_pti_adapter import (
    build_coconut_pti_packet,
    normalize_maturity_candidate,
)

TS = "2026-11-14T14:00:00+07:00"


class CoconutPtiAdapterTests(unittest.TestCase):
    def build(self, label="mature_green"):
        return build_coconut_pti_packet(
            VisionFinding(label, 0.91, "synthetic-image-001", (0.1, 0.2, 0.6, 0.8)),
            observation_id="obs-001",
            state_id="state-001",
            proposal_id="proposal-001",
            timestamp=TS,
        )

    def test_normalizes_four_project_maturity_classes(self):
        expected = {
            "young": "young_green",
            "young green": "young_green",
            "mature_green": "mature_green",
            "yellow": "yellow",
            "brown": "brown",
            "brown_aging": "brown",
        }
        for label, normalized in expected.items():
            with self.subTest(label=label):
                self.assertEqual(normalize_maturity_candidate(label), normalized)

    def test_unknown_label_remains_unknown(self):
        self.assertEqual(normalize_maturity_candidate("uncertain fruit"), "unknown")
        packet = self.build("uncertain fruit")
        self.assertEqual(
            packet["world_state"]["state"]["visual_maturity_candidate"], "unknown"
        )

    def test_packet_links_observation_world_state_and_review_proposal(self):
        packet = self.build()
        observation_id = packet["observation"]["observation_id"]
        self.assertEqual(packet["world_state"]["observation_refs"], [observation_id])
        self.assertEqual(packet["action_proposal"]["evidence_refs"], [observation_id])
        self.assertEqual(
            packet["action_proposal"]["proposed_action"],
            "request_human_maturity_review",
        )

    def test_uncalibrated_confidence_and_unknown_harvestability_are_preserved(self):
        packet = self.build()
        state = packet["world_state"]["state"]
        self.assertEqual(state["confidence_uncalibrated"], 0.91)
        self.assertEqual(state["harvestability"], "not_assessed")
        self.assertIsNone(state["height_m"])
        self.assertEqual(packet["world_state"]["freshness"], "unknown")

    def test_proposal_never_authorizes_actuation(self):
        packet = self.build()
        proposal = packet["action_proposal"]
        self.assertTrue(proposal["human_approval_required"])
        self.assertEqual(proposal["authority"], "advisory_only")
        self.assertFalse(proposal["actuation_allowed"])
        self.assertTrue(proposal["simulation_only"])
        self.assertFalse(packet["execution_authorized"])
        self.assertFalse(packet["physical_actuation_authorized"])

    def test_invalid_finding_is_rejected(self):
        with self.assertRaises(ValueError):
            build_coconut_pti_packet(
                VisionFinding("mature_green", float("nan"), "synthetic-image-001"),
                observation_id="obs-bad",
                state_id="state-bad",
                proposal_id="proposal-bad",
                timestamp=TS,
            )


if __name__ == "__main__":
    unittest.main()

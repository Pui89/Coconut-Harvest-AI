"""Standard-library tests for Coconut adoption of the PUI89 shared contract draft."""
import json
import unittest

from pui89_core.contracts import (
    ActionProposalRecord,
    FailureReport,
    Observation,
    SCHEMA_SOURCE_COMMIT,
    WorldStateRecord,
)
from pui89_autonomy.llm_interfaces import VisionFinding
from tools.pui89_coconut_contract_adapter import build_coconut_observation

TS = "2026-11-08T09:00:00+07:00"


class ObservationContractTests(unittest.TestCase):
    def make_observation(self, **changes):
        payload = dict(
            observation_id="obs-001",
            source="camera-01",
            modality="rgb",
            timestamp=TS,
            quality="unknown",
            provenance={"source_id": "image-001", "method": "manual_upload", "rights_status": "unknown"},
            integrity_status="unverified",
            value={"label": "mature_green"},
            confidence=0.82,
            uncertainty={"level": "unknown", "reason": "not calibrated"},
        )
        payload.update(changes)
        return Observation(**payload)

    def test_valid_observation_serializes_as_json(self):
        record = self.make_observation()
        data = json.loads(json.dumps(record.to_dict()))
        self.assertEqual(data["observation_id"], "obs-001")
        self.assertEqual(data["provenance"]["rights_status"], "unknown")
        self.assertEqual(data["integrity_status"], "unverified")

    def test_requires_provenance_and_valid_rights_status(self):
        with self.assertRaises(ValueError):
            self.make_observation(provenance={"source_id": "x", "method": "manual"})
        with self.assertRaises(ValueError):
            self.make_observation(provenance={
                "source_id": "x", "method": "manual", "rights_status": "approved"
            })

    def test_requires_value_or_payload_reference(self):
        with self.assertRaises(ValueError):
            self.make_observation(value=None, payload_ref=None)
        self.assertEqual(self.make_observation(value=None, payload_ref="sha256:abc").payload_ref, "sha256:abc")

    def test_rejects_invalid_modality_timestamp_and_confidence(self):
        for changes in (
            {"modality": "unknown_sensor"},
            {"timestamp": "2026-11-08T09:00:00"},
            {"confidence": float("nan")},
            {"confidence": True},
            {"confidence": 1.1},
        ):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.make_observation(**changes)

    def test_pinned_schema_revision_is_explicit(self):
        self.assertEqual(len(SCHEMA_SOURCE_COMMIT), 40)


class WorldStateContractTests(unittest.TestCase):
    def test_world_state_requires_unique_evidence_references_and_limits(self):
        record = WorldStateRecord(
            world_state_id="state-001", timestamp=TS, frame_id="camera-frame",
            state={"candidate_count": 1}, observation_refs=("obs-001",),
            freshness="unknown",
            uncertainty={"level": "unknown", "reason": "not measured"},
            limitations=("No detector accuracy claim",), unknown=("height_m",),
        )
        self.assertEqual(json.loads(json.dumps(record.to_dict()))["freshness"], "unknown")
        with self.assertRaises(ValueError):
            WorldStateRecord(
                world_state_id="state-002", timestamp=TS, frame_id="camera-frame",
                state={}, observation_refs=("obs-1", "obs-1"), freshness="fresh",
                uncertainty={"level": "low", "reason": "measured"},
                limitations=(),
            )


class ActionProposalContractTests(unittest.TestCase):
    def make_proposal(self, **changes):
        payload = dict(
            proposal_id="proposal-001", created_at=TS,
            proposed_action="request_human_inspection",
            rationale="Candidate evidence needs review",
            evidence_refs=("obs-001",), preconditions=("human reviewer available",),
            risk_level="unknown",
        )
        payload.update(changes)
        return ActionProposalRecord(**payload)

    def test_action_proposal_is_advisory_and_non_executable(self):
        data = json.loads(json.dumps(self.make_proposal().to_dict()))
        self.assertIs(data["human_approval_required"], True)
        self.assertEqual(data["authority"], "advisory_only")
        self.assertIs(data["actuation_allowed"], False)
        self.assertIs(data["simulation_only"], True)

    def test_action_proposal_rejects_unsafe_authority_and_empty_evidence(self):
        for changes in (
            {"human_approval_required": False},
            {"authority": "autonomous"},
            {"actuation_allowed": True},
            {"simulation_only": False},
            {"evidence_refs": ()},
        ):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.make_proposal(**changes)


class FailureReportContractTests(unittest.TestCase):
    def test_failure_report_records_unknown_safe_state_explicitly(self):
        report = FailureReport(
            failure_id="failure-001", reported_at=TS,
            failure_mode="source_provenance_missing", severity="medium",
            evidence_refs=("obs-001",), containment="hold candidate for review",
            recovery_recommendation="verify source and rights record",
            unresolved_uncertainty=("image reuse rights",), safe_state="unknown",
        )
        data = json.loads(json.dumps(report.to_dict()))
        self.assertEqual(data["safe_state"], "unknown")
        self.assertEqual(data["unresolved_uncertainty"], ["image reuse rights"])


class CoconutAdapterTests(unittest.TestCase):
    def test_maps_caller_supplied_finding_without_claiming_calibration(self):
        finding = VisionFinding("mature_green", 0.91, "image-001", (0.1, 0.2, 0.5, 0.8))
        record = build_coconut_observation(
            finding, observation_id="obs-coconut-001", timestamp=TS
        )
        self.assertEqual(record.modality, "rgb")
        self.assertEqual(record.provenance["rights_status"], "unknown")
        self.assertEqual(record.integrity_status, "unverified")
        self.assertEqual(record.uncertainty["level"], "unknown")
        self.assertIn("not established as calibrated", record.uncertainty["reason"])

    def test_rejects_invalid_finding_before_mapping(self):
        finding = VisionFinding(" ", float("nan"), " ")
        with self.assertRaises(ValueError):
            build_coconut_observation(
                finding, observation_id="obs-bad", timestamp=TS
            )


if __name__ == "__main__":
    unittest.main()

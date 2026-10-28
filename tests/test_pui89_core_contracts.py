"""Contract tests for the shared, dependency-light PUI89 AI Core."""
import json

import pytest

from pui89_core import (
    ActionProposal,
    TrackedObject,
    WorldState,
    propose_action,
    write_failure_report,
)


def test_world_state_round_trip_is_json_compatible():
    state = WorldState()
    state.upsert(
        TrackedObject(
            object_id="target-1",
            label="candidate",
            confidence=0.91,
            attributes={"source": "synthetic-test"},
        )
    )

    snapshot = state.to_dict()
    assert snapshot["objects"]["target-1"]["label"] == "candidate"
    assert snapshot["objects"]["target-1"]["confidence"] == pytest.approx(0.91)
    assert json.loads(json.dumps(snapshot))["task_status"] == "idle"


@pytest.mark.parametrize("confidence", [float("nan"), float("inf"), float("-inf"), -0.01, 1.01])
def test_tracked_object_rejects_invalid_confidence(confidence):
    with pytest.raises(ValueError):
        TrackedObject(
            object_id="target-invalid",
            label="synthetic-candidate",
            confidence=confidence,
        )


@pytest.mark.parametrize("confidence", [0.0, 1.0])
def test_tracked_object_accepts_confidence_boundaries(confidence):
    item = TrackedObject(
        object_id="target-boundary",
        label="synthetic-candidate",
        confidence=confidence,
    )
    assert item.confidence == confidence


@pytest.mark.parametrize("field,value", [("object_id", ""), ("label", "")])
def test_tracked_object_rejects_blank_identity_fields(field, value):
    arguments = {
        "object_id": "target-1",
        "label": "candidate",
        "confidence": 0.5,
    }
    arguments[field] = value
    with pytest.raises(ValueError):
        TrackedObject(**arguments)


def test_action_proposal_requires_review_and_is_not_executed():
    proposal = propose_action(
        action="inspect_target",
        rationale="Synthetic contract test only",
        confidence=0.85,
    )

    assert proposal.requires_human_review is True
    assert proposal.simulation_only is True
    assert proposal.executed is False


def test_action_proposal_rejects_non_simulation_execution():
    with pytest.raises(ValueError):
        ActionProposal(
            action="move",
            rationale="Must remain a proposal",
            confidence=0.9,
            simulation_only=False,
        )


def test_failure_report_is_written_as_valid_json(tmp_path):
    target = write_failure_report(
        tmp_path / "reports" / "failures.json",
        [{"code": "TEST_FAILURE", "message": "synthetic test failure"}],
        run_name="pui89-core-contract-test",
    )

    payload = json.loads(target.read_text(encoding="utf-8"))
    assert payload["run_name"] == "pui89-core-contract-test"
    assert payload["failure_count"] == 1
    assert payload["failures"][0]["code"] == "TEST_FAILURE"

from datetime import datetime, timezone

from pui89_core_v2.safety import evaluate_proposal


NOW = datetime(2026, 11, 8, 10, 0, tzinfo=timezone.utc)


def valid_inputs():
    observation = {
        "observation_id": "obs-001",
        "status": "valid",
        "source": {"integrity_status": "verified"},
    }
    state = {
        "state_id": "state-001",
        "status": "CURRENT",
        "created_at": "2026-11-08T09:59:50+00:00",
        "claims": [{
            "claim_id": "claim-001",
            "value_status": "KNOWN",
            "evidence_ids": ["obs-001"],
        }],
    }
    proposal = {
        "proposal_id": "proposal-001",
        "project_id": "coconut-harvest-ai",
        "world_state_id": "state-001",
        "intent": "Request a human-reviewed harvesting plan",
        "preconditions": ["worker exclusion zone confirmed"],
        "supporting_observation_ids": ["obs-001"],
        "risk": {"level": "low", "hazards": [], "mitigations": []},
        "authorization": {"required": True, "status": "approved"},
        "decision": "PROPOSED",
    }
    return proposal, state, [observation]


def test_complete_low_risk_proposal_passes_only_to_human_review():
    proposal, state, observations = valid_inputs()
    result = evaluate_proposal(
        proposal, state, observations, human_authorized=True, now=NOW
    )
    assert result.decision == "ALLOW_FOR_HUMAN_REVIEW"
    assert "no_execution_performed" in result.reasons[0]


def test_missing_human_authorization_holds():
    proposal, state, observations = valid_inputs()
    result = evaluate_proposal(proposal, state, observations, now=NOW)
    assert result.decision == "HOLD"
    assert "human_authorization_not_supplied_to_gate" in result.reasons


def test_stale_world_state_holds():
    proposal, state, observations = valid_inputs()
    state["created_at"] = "2026-11-08T09:00:00+00:00"
    result = evaluate_proposal(
        proposal, state, observations, human_authorized=True, now=NOW
    )
    assert result.decision == "HOLD"
    assert "world_state_stale" in result.reasons


def test_conflicted_claim_holds():
    proposal, state, observations = valid_inputs()
    state["claims"][0]["value_status"] = "CONFLICTED"
    result = evaluate_proposal(
        proposal, state, observations, human_authorized=True, now=NOW
    )
    assert result.decision == "HOLD"
    assert "claim_0_conflicted" in result.reasons


def test_unverified_observation_holds():
    proposal, state, observations = valid_inputs()
    observations[0]["source"]["integrity_status"] = "unverified"
    result = evaluate_proposal(
        proposal, state, observations, human_authorized=True, now=NOW
    )
    assert result.decision == "HOLD"
    assert "supporting_observation_provenance_not_verified" in result.reasons


def test_high_risk_proposal_holds():
    proposal, state, observations = valid_inputs()
    proposal["risk"]["level"] = "high"
    result = evaluate_proposal(
        proposal, state, observations, human_authorized=True, now=NOW
    )
    assert result.decision == "HOLD"
    assert "risk_level_requires_hold" in result.reasons


def test_mismatched_world_state_holds():
    proposal, state, observations = valid_inputs()
    proposal["world_state_id"] = "another-state"
    result = evaluate_proposal(
        proposal, state, observations, human_authorized=True, now=NOW
    )
    assert result.decision == "HOLD"
    assert "world_state_reference_mismatch" in result.reasons


def test_invalid_clock_timezone_holds():
    proposal, state, observations = valid_inputs()
    naive_now = datetime(2026, 11, 8, 10, 0)
    result = evaluate_proposal(
        proposal, state, observations, human_authorized=True, now=naive_now
    )
    assert result.decision == "HOLD"
    assert "evaluation_clock_must_be_timezone_aware" in result.reasons

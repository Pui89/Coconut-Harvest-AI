from agents.harvest_planning_agent import (
    AgentConfig,
    CoconutCandidate,
    assess_candidate,
    propose_plan,
)


def test_eligible_candidate_requires_explicit_reachability():
    candidate = CoconutCandidate("A", 0.9, 1.0, 0.0, 1.0, reachable=True)
    assert assess_candidate(candidate).status == "ELIGIBLE_FOR_SIMULATION_REVIEW"


def test_missing_position_is_rejected_by_default():
    candidate = CoconutCandidate("A", 0.9, reachable=True)
    result = assess_candidate(candidate)
    assert result.status == "REJECTED"
    assert any("3D position missing" in reason for reason in result.reasons)


def test_unknown_reachability_is_rejected():
    candidate = CoconutCandidate("A", 0.9, 1.0, 0.0, 1.0, reachable=None)
    result = assess_candidate(candidate)
    assert result.status == "REJECTED"
    assert any("reachability" in reason for reason in result.reasons)


def test_low_confidence_and_occlusion_are_rejected():
    candidate = CoconutCandidate(
        "A", 0.2, 1.0, 0.0, 1.0, reachable=True, occluded=True
    )
    result = assess_candidate(candidate)
    assert result.status == "REJECTED"
    assert len(result.reasons) >= 2


def test_out_of_range_candidate_is_rejected():
    candidate = CoconutCandidate("A", 0.9, 4.0, 0.0, 0.0, reachable=True)
    assert assess_candidate(candidate).status == "REJECTED"


def test_agent_selects_highest_confidence_eligible_candidate():
    report = propose_plan([
        CoconutCandidate("near", 0.75, 1.0, 0.0, 1.0, reachable=True),
        CoconutCandidate("high", 0.95, 1.5, 0.0, 1.0, reachable=True),
        CoconutCandidate("unknown", 0.99, 1.0, 0.0, 1.0, reachable=None),
    ])
    assert report["recommended_target_id"] == "high"
    assert report["status"] == "PROPOSAL_ONLY"
    assert report["safety_boundary"]["actuator_commands_sent"] is False
    assert report["safety_boundary"]["physical_robot_authorized"] is False


def test_no_eligible_targets_produces_safe_hold():
    report = propose_plan([
        CoconutCandidate("unknown", 0.99, 1.0, 0.0, 1.0, reachable=None)
    ])
    assert report["status"] == "SAFE_HOLD"
    assert report["recommended_target_id"] is None


def test_configurable_confidence_threshold():
    candidate = CoconutCandidate("A", 0.7, 1.0, 0.0, 1.0, reachable=True)
    config = AgentConfig(min_confidence=0.8)
    assert assess_candidate(candidate, config).status == "REJECTED"

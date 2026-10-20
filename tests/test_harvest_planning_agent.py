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


def test_mature_only_mode_excludes_young_and_keeps_mature_green_and_brown():
    report = propose_plan([
        CoconutCandidate("young", 0.95, 1.0, 0.0, 1.0, reachable=True, stage="young_green"),
        CoconutCandidate("green-mature", 0.90, 1.0, 0.0, 1.0, reachable=True, stage="mature_green"),
        CoconutCandidate("brown-mature", 0.92, 1.2, 0.0, 1.0, reachable=True, stage="mature_brown_or_dry"),
    ], harvest_mode="all_mature")
    assert report["eligible_target_ids"] == ["brown-mature", "green-mature"]
    assert report["selected_stages"] == ["mature_brown_or_dry", "mature_green"]
    assert "young" not in report["eligible_target_ids"]


def test_young_only_mode_does_not_select_mature_fruit():
    report = propose_plan([
        CoconutCandidate("young", 0.91, 1.0, 0.0, 1.0, reachable=True, stage="young_green"),
        CoconutCandidate("mature", 0.99, 1.0, 0.0, 1.0, reachable=True, stage="mature_green"),
    ], harvest_mode="young_green")
    assert report["eligible_target_ids"] == ["young"]


def test_uncertain_stage_is_rejected_when_operator_selects_a_harvest_mode():
    report = propose_plan([
        CoconutCandidate("unknown", 0.99, 1.0, 0.0, 1.0, reachable=True, stage="uncertain_stage")
    ], harvest_mode="all_mature")
    assert report["status"] == "SAFE_HOLD"
    assert report["recommended_target_id"] is None
    assert any("human review" in reason for reason in report["assessments"][0]["reasons"])


def test_survey_only_never_proposes_harvest():
    report = propose_plan([
        CoconutCandidate("brown", 0.99, 1.0, 0.0, 1.0, reachable=True, stage="mature_brown_or_dry")
    ], harvest_mode="survey_only")
    assert report["status"] == "SAFE_HOLD"
    assert report["recommended_target_id"] is None


def test_selected_combination_requires_explicit_safe_stages():
    report = propose_plan([
        CoconutCandidate("green", 0.91, 1.0, 0.0, 1.0, reachable=True, stage="mature_green"),
        CoconutCandidate("brown", 0.92, 1.2, 0.0, 1.0, reachable=True, stage="mature_brown_or_dry"),
    ], harvest_mode="selected_combination", selected_stages=["mature_green", "mature_brown_or_dry"])
    assert set(report["eligible_target_ids"]) == {"green", "brown"}

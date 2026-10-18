from math import nan, inf

from coconut_harvest_robot.harvestability import HarvestDecision,HarvestEvidence,score_harvestability
from coconut_harvest_robot.safety_gate import ActionCandidate,SafetyDecision,validate_action

def test_low_confidence_abstains():
    r=score_harvestability(HarvestEvidence(.5,.5,.5,.5,.5,sensor_quality=.8))
    assert r.decision==HarvestDecision.LOW_CONFIDENCE

def test_safety_blocks_human_exclusion():
    r=validate_action(ActionCandidate("c1",.95,.5,.1,100,5,human_in_exclusion_zone=True))
    assert r.decision==SafetyDecision.BLOCK

def test_safety_approves_safe_candidate():
    r=validate_action(ActionCandidate("c1",.95,.5,.1,100,5))
    assert r.decision==SafetyDecision.APPROVE


def test_safety_blocks_non_finite_or_out_of_range_parameters():
    unsafe = [
        ActionCandidate("c1", nan, .5, .1, 100, 5),
        ActionCandidate("c1", .95, .5, nan, 100, 5),
        ActionCandidate("c1", .95, .5, .1, inf, 5),
        ActionCandidate("c1", .95, .5, .1, 100, nan),
        ActionCandidate("c1", 1.01, .5, .1, 100, 5),
        ActionCandidate("c1", .95, .5, -0.1, 100, 5),
        ActionCandidate("c1", .95, .5, .1, -1, 5),
        ActionCandidate("c1", .95, .5, .1, 100, -1),
        ActionCandidate("", .95, .5, .1, 100, 5),
    ]
    for candidate in unsafe:
        result = validate_action(candidate)
        assert result.decision == SafetyDecision.BLOCK, candidate
        assert result.reasons


def test_safety_still_blocks_emergency_stop_and_collision():
    for candidate in (
        ActionCandidate("c1", .95, .5, .1, 100, 5, emergency_stop=True),
        ActionCandidate("c1", .95, .5, .1, 100, 5, collision_free=False),
    ):
        assert validate_action(candidate).decision == SafetyDecision.BLOCK

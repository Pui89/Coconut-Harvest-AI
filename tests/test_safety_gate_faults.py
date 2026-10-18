from dataclasses import replace
import math

import pytest

from coconut_harvest_robot.safety_gate import (
    ActionCandidate,
    SafetyDecision,
    validate_action,
)


def valid_candidate() -> ActionCandidate:
    return ActionCandidate(
        target_id="test-target",
        confidence=0.95,
        clearance_m=0.5,
        speed_mps=0.1,
        force_n=50.0,
        height_m=5.0,
        collision_free=True,
    )


def test_valid_candidate_is_approved_by_prototype_gate():
    result = validate_action(valid_candidate())
    assert result.decision is SafetyDecision.APPROVE
    assert result.reasons == ()


@pytest.mark.parametrize(
    ("field", "value"),
    [
        (field, value)
        for field in ("confidence", "clearance_m", "speed_mps", "force_n", "height_m")
        for value in (math.nan, math.inf, -math.inf)
    ],
)
def test_non_finite_action_values_fail_closed(field: str, value: float):
    result = validate_action(replace(valid_candidate(), **{field: value}))
    assert result.decision is SafetyDecision.BLOCK
    assert any("non-finite numeric value" in reason for reason in result.reasons)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("confidence", -0.01),
        ("confidence", 1.01),
        ("clearance_m", -0.01),
        ("speed_mps", -0.01),
        ("force_n", -0.01),
        ("height_m", -0.01),
    ],
)
def test_out_of_domain_action_values_fail_closed(field: str, value: float):
    result = validate_action(replace(valid_candidate(), **{field: value}))
    assert result.decision is SafetyDecision.BLOCK


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("emergency_stop", True, "emergency stop active"),
        ("human_in_exclusion_zone", True, "human detected in exclusion zone"),
        ("collision_free", False, "collision check failed"),
        ("confidence", 0.79, "confidence below execution threshold"),
        ("clearance_m", 0.19, "workspace clearance too small"),
        ("speed_mps", 0.51, "speed exceeds limit"),
        ("force_n", 500.1, "force exceeds limit"),
        ("height_m", 14.1, "workspace height exceeds limit"),
    ],
)
def test_existing_safety_conditions_still_block(field, value, reason):
    result = validate_action(replace(valid_candidate(), **{field: value}))
    assert result.decision is SafetyDecision.BLOCK
    assert reason in result.reasons

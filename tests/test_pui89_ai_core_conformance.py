"""Cross-project conformance tests for the PUI89 simulation-only action policy.

These tests exercise the same contract in each repository without downloading models,
installing optional dependencies, accessing the network, or calling hardware.
"""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "pui89_autonomy_lab.py"
SPEC = importlib.util.spec_from_file_location("pui89_autonomy_lab_conformance", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
MockVLA = MODULE.MockVLA

REQUIRED_FLAGS = {
    "emergency_stop": False,
    "sensors_ok": True,
    "sensor_data_fresh": True,
    "comms_ok": True,
}
READY_STATE = {
    **REQUIRED_FLAGS,
    "target_visible": True,
    "target_valid": True,
    "human_review_required": False,
    "operator_approved": True,
    "confidence": 0.95,
}


def test_healthy_state_returns_simulation_only_proposal() -> None:
    action, trace = MockVLA().propose(dict(READY_STATE), "SIMULATED_TASK")
    assert action == "SIMULATED_TASK"
    assert "simulation_only_action" in trace


@pytest.mark.parametrize("flag", sorted(REQUIRED_FLAGS))
def test_missing_required_safety_flag_fails_closed(flag: str) -> None:
    state = dict(READY_STATE)
    state.pop(flag)
    action, trace = MockVLA().propose(state, "SIMULATED_TASK")
    assert action == "SAFE_HOLD"
    assert any(flag in item for item in trace)


@pytest.mark.parametrize("bad_value", ["false", "true", 0, 1, None, [], {}])
def test_malformed_required_safety_telemetry_fails_closed(bad_value: object) -> None:
    for flag in REQUIRED_FLAGS:
        state = dict(READY_STATE)
        state[flag] = bad_value
        action, _ = MockVLA().propose(state, "SIMULATED_TASK")
        assert action == "SAFE_HOLD", flag


@pytest.mark.parametrize(
    ("flag", "bad_value"),
    [
        ("emergency_stop", True),
        ("sensors_ok", False),
        ("sensor_data_fresh", False),
        ("comms_ok", False),
    ],
)
def test_active_safety_fault_fails_closed(flag: str, bad_value: bool) -> None:
    state = {**READY_STATE, flag: bad_value}
    action, _ = MockVLA().propose(state, "SIMULATED_TASK")
    assert action == "SAFE_HOLD"


def test_missing_confidence_abstains_instead_of_assuming_perfect_confidence() -> None:
    state = dict(READY_STATE)
    state.pop("confidence")
    action, trace = MockVLA().propose(state, "SIMULATED_TASK")
    assert action == "UNKNOWN"
    assert any("confidence_missing" in item for item in trace)


@pytest.mark.parametrize("confidence", [True, False, "0.9", None, -0.01, 1.01, math.nan, math.inf, -math.inf])
def test_invalid_confidence_abstains(confidence: object) -> None:
    state = {**READY_STATE, "confidence": confidence}
    action, _ = MockVLA().propose(state, "SIMULATED_TASK")
    assert action == "UNKNOWN"


def test_low_confidence_abstains() -> None:
    action, _ = MockVLA().propose({**READY_STATE, "confidence": 0.1}, "SIMULATED_TASK")
    assert action == "UNKNOWN"


@pytest.mark.parametrize("uncertainty_flag", ["modalities_conflict", "missing_required_modality"])
def test_uncertain_or_incomplete_perception_abstains(uncertainty_flag: str) -> None:
    action, _ = MockVLA().propose({**READY_STATE, uncertainty_flag: True}, "SIMULATED_TASK")
    assert action == "UNKNOWN"


def test_required_human_review_is_not_bypassed() -> None:
    action, _ = MockVLA().propose({**READY_STATE, "human_review_required": True}, "SIMULATED_TASK")
    assert action == "REQUEST_HUMAN_REVIEW"


def test_high_impact_action_label_is_blocked() -> None:
    action, _ = MockVLA().propose(READY_STATE, "REQUEST_ENFORCEMENT")
    assert action == "REQUEST_HUMAN_REVIEW"


def test_invalid_state_object_fails_closed() -> None:
    action, _ = MockVLA().propose(None, "SIMULATED_TASK")  # type: ignore[arg-type]
    assert action == "SAFE_HOLD"

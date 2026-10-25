"""Safety-gated symbolic proposals for simulation only; no actuator interfaces."""
from __future__ import annotations

import math
from typing import Any

ALLOWED_READY_ACTIONS = {
    "HARVEST_STEP_SIMULATION_ONLY",
    "PLAN_RESCUE_ROUTE_SIMULATION_ONLY",
    "REQUEST_HUMAN_REVIEW",
}
SAFE_HOLD = "SAFE_HOLD"
UNKNOWN = "UNKNOWN"


def evaluate_world_state(
    state: dict[str, Any],
    *,
    ready_action: str,
    confidence_threshold: float = 0.65,
) -> dict[str, Any]:
    """Convert state metadata into a bounded, human-readable simulation proposal.

    This function never emits velocity, actuator, navigation-goal, MAVLink,
    cutter, alarm, or enforcement commands.
    """
    if ready_action not in ALLOWED_READY_ACTIONS:
        raise ValueError(f"ready_action must be one of {sorted(ALLOWED_READY_ACTIONS)}")
    if not math.isfinite(float(confidence_threshold)) or not 0.0 <= confidence_threshold <= 1.0:
        raise ValueError("confidence_threshold must be finite and within [0, 1]")

    def result(action: str, reason: str) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "action": action,
            "reason_codes": [reason],
            "hardware_actuation": False,
            "simulation_only": True,
        }

    if state.get("emergency_stop", False):
        return result(SAFE_HOLD, "EMERGENCY_STOP_REPORTED")
    for key, reason in (
        ("sensors_ok", "SENSOR_FAULT"),
        ("sensor_data_fresh", "STALE_SENSOR_DATA"),
        ("comms_ok", "COMMUNICATIONS_LOST"),
        ("battery_ok", "BATTERY_STATUS_UNSAFE"),
        ("propulsion_ok", "PROPULSION_STATUS_UNSAFE"),
    ):
        if state.get(key, True) is False:
            return result(SAFE_HOLD, reason)

    if state.get("modalities_conflict", False):
        return result(UNKNOWN, "MODALITIES_CONFLICT")
    if state.get("missing_required_modality", False):
        return result(UNKNOWN, "REQUIRED_MODALITY_MISSING")

    confidence = state.get("confidence", 1.0)
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
        return result(UNKNOWN, "CONFIDENCE_MISSING_OR_INVALID")
    if not math.isfinite(float(confidence)) or not 0.0 <= confidence <= 1.0:
        return result(UNKNOWN, "CONFIDENCE_OUT_OF_RANGE")
    if confidence < confidence_threshold:
        return result(UNKNOWN, "CONFIDENCE_BELOW_THRESHOLD")

    if state.get("target_visible", True) is False or state.get("target_valid", True) is False:
        return result("SEARCH", "TARGET_NOT_AVAILABLE")
    if state.get("human_review_required", False):
        return result("REQUEST_HUMAN_REVIEW", "HUMAN_REVIEW_REQUIRED")
    if state.get("operator_approved", True) is False:
        return result("REQUEST_APPROVAL", "OPERATOR_APPROVAL_MISSING")

    return result(ready_action, "SIMULATION_ONLY_PROPOSAL_READY")

"""Shared fail-closed health gate for simulation proposals only.

This module never commands hardware. A positive decision means only that the
supplied software telemetry is adequate to propose a simulation step.
"""
from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any

REQUIRED_BOOLEAN_FIELDS = (
    "emergency_stop",
    "sensors_ok",
    "sensor_data_fresh",
    "perception_ok",
    "localization_ok",
    "comms_ok",
    "safety_monitor_ok",
    "operator_approved",
)


def assess_health(
    snapshot: Mapping[str, Any] | None,
    minimum_confidence: float = 0.75,
) -> dict[str, Any]:
    """Assess telemetry conservatively; never grants physical actuation."""
    if (
        isinstance(minimum_confidence, bool)
        or not isinstance(minimum_confidence, (int, float))
        or not math.isfinite(minimum_confidence)
        or not 0.0 <= minimum_confidence <= 1.0
    ):
        raise ValueError("minimum_confidence must be finite and within [0, 1]")

    if not isinstance(snapshot, Mapping):
        return _decision("SAFE_HOLD", ["telemetry_missing_or_not_a_mapping"])

    malformed = [
        key for key in REQUIRED_BOOLEAN_FIELDS
        if key not in snapshot or not isinstance(snapshot[key], bool)
    ]
    if malformed:
        return _decision("SAFE_HOLD", ["missing_or_malformed:" + ",".join(malformed)])

    confidence = snapshot.get("confidence")
    if (
        isinstance(confidence, bool)
        or not isinstance(confidence, (int, float))
        or not math.isfinite(confidence)
        or not 0.0 <= confidence <= 1.0
    ):
        return _decision("SAFE_HOLD", ["confidence_missing_or_invalid"])

    if snapshot["emergency_stop"]:
        return _decision("STOPPED", ["emergency_stop_active"])
    if not snapshot["safety_monitor_ok"]:
        return _decision("STOPPED", ["safety_monitor_unhealthy"])

    if not snapshot["operator_approved"]:
        return _decision("REQUEST_HUMAN_REVIEW", ["operator_approval_missing"])

    blockers = [
        key for key in (
            "sensors_ok", "sensor_data_fresh", "perception_ok",
            "localization_ok", "comms_ok",
        )
        if not snapshot[key]
    ]
    if blockers:
        return _decision("SAFE_HOLD", ["health_gate_failed:" + ",".join(blockers)])

    if confidence < minimum_confidence:
        return _decision("REQUEST_HUMAN_REVIEW", ["confidence_below_threshold"])

    return _decision("SIMULATION_READY", ["software_health_gates_passed_simulation_only"])


def _decision(mode: str, reasons: list[str]) -> dict[str, Any]:
    return {
        "mode": mode,
        "reasons": reasons,
        "simulation_only": True,
        "physical_actuation_permitted": False,
    }

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum


class SafetyDecision(str, Enum):
    APPROVE = "APPROVE"
    BLOCK = "BLOCK"


@dataclass(frozen=True)
class SafetyLimits:
    min_clearance_m: float = 0.20
    max_speed_mps: float = 0.50
    max_force_n: float = 500.0
    max_workspace_height_m: float = 14.0


@dataclass(frozen=True)
class ActionCandidate:
    target_id: str
    confidence: float
    clearance_m: float
    speed_mps: float
    force_n: float
    height_m: float
    emergency_stop: bool = False
    human_in_exclusion_zone: bool = False
    collision_free: bool = True


@dataclass(frozen=True)
class SafetyResult:
    decision: SafetyDecision
    reasons: tuple[str, ...]


def validate_action(
    a: ActionCandidate,
    limits: SafetyLimits = SafetyLimits(),
) -> SafetyResult:
    """Fail closed when action evidence is unsafe or numerically invalid.

    This software gate is a prototype check, not a certified safety controller.
    """
    reasons: list[str] = []

    numeric_values = {
        "confidence": a.confidence,
        "clearance_m": a.clearance_m,
        "speed_mps": a.speed_mps,
        "force_n": a.force_n,
        "height_m": a.height_m,
        "min_clearance_m": limits.min_clearance_m,
        "max_speed_mps": limits.max_speed_mps,
        "max_force_n": limits.max_force_n,
        "max_workspace_height_m": limits.max_workspace_height_m,
    }
    invalid_values = [
        name for name, value in numeric_values.items()
        if not math.isfinite(value)
    ]
    if invalid_values:
        reasons.append(
            "non-finite numeric value: " + ", ".join(invalid_values)
        )

    if not 0.0 <= a.confidence <= 1.0:
        reasons.append("confidence outside [0, 1]")
    if a.clearance_m < 0.0:
        reasons.append("workspace clearance is negative")
    if a.speed_mps < 0.0:
        reasons.append("speed is negative")
    if a.force_n < 0.0:
        reasons.append("force is negative")
    if a.height_m < 0.0:
        reasons.append("workspace height is negative")

    if a.emergency_stop:
        reasons.append("emergency stop active")
    if a.human_in_exclusion_zone:
        reasons.append("human detected in exclusion zone")
    if not a.collision_free:
        reasons.append("collision check failed")
    if a.confidence < 0.80:
        reasons.append("confidence below execution threshold")
    if a.clearance_m < limits.min_clearance_m:
        reasons.append("workspace clearance too small")
    if a.speed_mps > limits.max_speed_mps:
        reasons.append("speed exceeds limit")
    if a.force_n > limits.max_force_n:
        reasons.append("force exceeds limit")
    if a.height_m > limits.max_workspace_height_m:
        reasons.append("workspace height exceeds limit")

    return SafetyResult(
        SafetyDecision.BLOCK if reasons else SafetyDecision.APPROVE,
        tuple(dict.fromkeys(reasons)),
    )

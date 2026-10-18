from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite
from numbers import Real


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


def _valid_number(value: object) -> bool:
    """Accept finite real numbers only; reject bools, strings, NaN and infinity."""
    return isinstance(value, Real) and not isinstance(value, bool) and isfinite(value)


def validate_action(
    a: ActionCandidate, limits: SafetyLimits = SafetyLimits()
) -> SafetyResult:
    """Fail closed when an action parameter or configured limit is invalid.

    This software gate is a defence-in-depth check, not a certified safety
    controller and not authorization to operate a physical cutter or arm.
    """
    reasons: list[str] = []

    limit_values = (
        limits.min_clearance_m,
        limits.max_speed_mps,
        limits.max_force_n,
        limits.max_workspace_height_m,
    )
    if not all(_valid_number(value) for value in limit_values):
        reasons.append("safety limits contain invalid numeric values")
    elif (
        limits.min_clearance_m < 0
        or limits.max_speed_mps <= 0
        or limits.max_force_n <= 0
        or limits.max_workspace_height_m <= 0
    ):
        reasons.append("safety limits are outside allowed ranges")

    if not isinstance(a.target_id, str) or not a.target_id.strip():
        reasons.append("target identifier missing")
    if a.emergency_stop:
        reasons.append("emergency stop active")
    if a.human_in_exclusion_zone:
        reasons.append("human detected in exclusion zone")
    if not a.collision_free:
        reasons.append("collision check failed")

    if not _valid_number(a.confidence) or not 0.0 <= a.confidence <= 1.0:
        reasons.append("confidence is invalid")
    elif a.confidence < 0.80:
        reasons.append("confidence below execution threshold")

    if not _valid_number(a.clearance_m) or a.clearance_m < 0:
        reasons.append("workspace clearance is invalid")
    elif a.clearance_m < limits.min_clearance_m:
        reasons.append("workspace clearance too small")

    if not _valid_number(a.speed_mps) or a.speed_mps < 0:
        reasons.append("speed is invalid")
    elif a.speed_mps > limits.max_speed_mps:
        reasons.append("speed exceeds limit")

    if not _valid_number(a.force_n) or a.force_n < 0:
        reasons.append("force is invalid")
    elif a.force_n > limits.max_force_n:
        reasons.append("force exceeds limit")

    if not _valid_number(a.height_m) or a.height_m < 0:
        reasons.append("workspace height is invalid")
    elif a.height_m > limits.max_workspace_height_m:
        reasons.append("workspace height exceeds limit")

    return SafetyResult(
        SafetyDecision.BLOCK if reasons else SafetyDecision.APPROVE,
        tuple(reasons),
    )

"""Conservative autonomy supervisor for software-level decision gating.

This module proposes a system mode from explicit health/status inputs. It does
not operate hardware, command actuators, perform perception, or replace an
independent safety controller.
"""
from dataclasses import dataclass
from enum import Enum
import math


class Mode(str, Enum):
    AUTONOMOUS_CANDIDATE = "autonomous_candidate"
    SAFE_HOLD = "safe_hold"
    MANUAL_RECOVERY = "manual_recovery"
    STOPPED = "stopped"


@dataclass(frozen=True)
class SystemStatus:
    perception_ok: bool
    localization_ok: bool
    communication_ok: bool
    safety_monitor_ok: bool
    operator_authorized: bool
    emergency_stop: bool
    hazard_clear: bool
    task_request_valid: bool
    confidence: float


@dataclass(frozen=True)
class SupervisorDecision:
    mode: Mode
    reasons: tuple[str, ...]
    permitted_next_steps: tuple[str, ...]


def evaluate_status(status: SystemStatus, minimum_confidence: float = 0.75) -> SupervisorDecision:
    """Return a conservative advisory mode; never issue physical commands."""
    if not math.isfinite(minimum_confidence) or not 0.0 <= minimum_confidence <= 1.0:
        raise ValueError("minimum_confidence must be finite and within [0, 1]")
    if not math.isfinite(status.confidence) or not 0.0 <= status.confidence <= 1.0:
        return SupervisorDecision(
            Mode.SAFE_HOLD,
            ("confidence is non-finite or outside [0, 1]",),
            ("withhold automated task approval", "request human review"),
        )

    if status.emergency_stop:
        return SupervisorDecision(
            Mode.STOPPED,
            ("emergency stop is active",),
            ("maintain stop through an independent safety system", "notify operator if available"),
        )
    if not status.safety_monitor_ok:
        return SupervisorDecision(
            Mode.STOPPED,
            ("safety monitor health is not confirmed",),
            ("maintain stop through an independent safety system", "request manual recovery"),
        )
    if not status.operator_authorized or not status.task_request_valid:
        reasons = []
        if not status.operator_authorized:
            reasons.append("operator authorization is missing")
        if not status.task_request_valid:
            reasons.append("task request is invalid or unverified")
        return SupervisorDecision(
            Mode.MANUAL_RECOVERY,
            tuple(reasons),
            ("withhold automated task approval", "request authorized human review"),
        )

    blockers = []
    if not status.perception_ok:
        blockers.append("perception health is not confirmed")
    if not status.localization_ok:
        blockers.append("localization health is not confirmed")
    if not status.communication_ok:
        blockers.append("required communication link is unavailable")
    if not status.hazard_clear:
        blockers.append("hazard clearance is not confirmed")
    if status.confidence < minimum_confidence:
        blockers.append("confidence is below the configured threshold")
    if blockers:
        return SupervisorDecision(
            Mode.SAFE_HOLD,
            tuple(blockers),
            ("do not start or continue the hazardous task", "hold only if independently verified safe", "notify operator or enter manual recovery"),
        )

    return SupervisorDecision(
        Mode.AUTONOMOUS_CANDIDATE,
        ("all supplied software gates passed; this is not hardware safety certification",),
        ("allow the application to propose the next bounded step", "continue independent monitoring", "require separate hardware interlocks for physical action"),
    )

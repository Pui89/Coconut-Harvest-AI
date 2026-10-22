"""Conservative decision-support agent for Coconut Harvest AI.

This module does not control actuators or claim a trained detector exists.
It converts supplied perception/robot-state measurements into reviewable
recommendations. Standard-library only; no network calls.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class AgentDecision:
    project: str
    status: str
    recommendation: str
    reasons: tuple[str, ...]
    requires_human_approval: bool = True
    actuator_command: None = None

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["reasons"] = list(self.reasons)
        return result


def run_agent(observation: dict[str, Any]) -> AgentDecision:
    """Assess one candidate harvest target; never issue a robot motion command.

    Expected optional keys: target_detected, confidence (0..1), depth_m,
    reachable, obstacle_clear, sensor_ok, human_approved.
    """
    if not isinstance(observation, dict):
        raise TypeError("observation must be a dictionary")

    reasons: list[str] = []
    if observation.get("sensor_ok") is False:
        return AgentDecision("coconut-harvest", "STOP", "STOP_AND_CHECK_SENSORS",
                             ("Sensor health check failed.",))
    if not observation.get("target_detected", False):
        return AgentDecision("coconut-harvest", "NEED_DATA", "REQUEST_NEW_VIEW",
                             ("No target detection was supplied.",))
    confidence = observation.get("confidence")
    if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 1:
        return AgentDecision("coconut-harvest", "NEED_DATA", "REQUEST_VALID_CONFIDENCE",
                             ("Confidence must be a numeric value from 0 to 1.",))
    if confidence < 0.80:
        return AgentDecision("coconut-harvest", "REVIEW", "REQUEST_SECOND_VIEW",
                             ("Target confidence is below the configured 0.80 review threshold.",))
    depth = observation.get("depth_m")
    if not isinstance(depth, (int, float)) or isinstance(depth, bool) or depth <= 0:
        return AgentDecision("coconut-harvest", "NEED_DATA", "REQUEST_VALID_DEPTH",
                             ("A positive, valid depth measurement is required.",))
    if observation.get("reachable") is not True:
        return AgentDecision("coconut-harvest", "REVIEW", "REPLAN_OR_SKIP_TARGET",
                             ("Reachability has not been confirmed.",))
    if observation.get("obstacle_clear") is not True:
        return AgentDecision("coconut-harvest", "STOP", "HOLD_AND_REASSESS",
                             ("Obstacle clearance is not confirmed.",))
    reasons.append("Perception, depth, reachability, and obstacle checks passed for this supplied observation.")
    if observation.get("human_approved") is not True:
        return AgentDecision("coconut-harvest", "AWAITING_APPROVAL", "REQUEST_HUMAN_APPROVAL",
                             tuple(reasons + ["No actuator command is generated; human approval is still required."]))
    return AgentDecision("coconut-harvest", "READY_FOR_EXTERNAL_CONTROLLER",
                         "PASS_REVIEW_GATE_ONLY",
                         tuple(reasons + ["Approval recorded; a separate validated controller must decide any motion."]))

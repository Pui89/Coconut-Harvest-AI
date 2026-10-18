"""Safety-gated end-to-end orchestration for simulation and research.

This module creates a proposal/report only. It does not connect to ROS 2,
motors, cutters, grippers, or other actuators. The existing trajectory planner
is a prototype and is not accepted as proof of collision-free motion.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any

import torch

from coconut_harvest_robot.config import RobotConfig
from coconut_harvest_robot.harvestability import HarvestDecision, HarvestEvidence, score_harvestability
from coconut_harvest_robot.pipeline import HarvestPipeline
from coconut_harvest_robot.safety_gate import ActionCandidate, SafetyDecision, SafetyLimits, validate_action
from coconut_harvest_robot.sensor_quality import SensorObservation, SensorStatus, assess_sensor_health


@dataclass(frozen=True)
class EndToEndReport:
    status: str
    sensor_status: str
    sensor_quality: float
    harvestability_decision: str
    harvestability_score: float
    safety_decision: str
    safety_reasons: tuple[str, ...]
    perception_summary: str
    trajectory_waypoint_count: int
    trajectory_is_verified: bool
    actuator_commands_sent: bool
    notes: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run_end_to_end(
    rgb: torch.Tensor,
    depth: torch.Tensor,
    instruction: str,
    sensor_observations: list[SensorObservation],
    evidence: HarvestEvidence,
    candidate: ActionCandidate,
    *,
    collision_check_passed: bool = False,
    config: RobotConfig | None = None,
    pipeline: HarvestPipeline | None = None,
) -> EndToEndReport:
    """Run sensor gate, perception proposal, harvestability, and safety gate.

    collision_check_passed must only be true when an independent, trusted
    collision checker has actually evaluated the candidate trajectory. The
    repository's current simplified planner does not qualify as that checker.
    No actuator command is ever sent by this function.
    """
    health = assess_sensor_health(sensor_observations)
    effective_evidence = replace(
        evidence,
        sensor_quality=min(evidence.sensor_quality, health.quality),
    )
    harvestability = score_harvestability(effective_evidence)

    active_pipeline = pipeline or HarvestPipeline(
        config=config or RobotConfig(rrt_iterations=32)
    )
    active_pipeline.eval()
    with torch.inference_mode():
        result = active_pipeline(rgb, depth, instruction)

    reasons: list[str] = []
    if health.status != SensorStatus.OK:
        reasons.append("sensor health is not OK; safe hold required")
    if harvestability.decision != HarvestDecision.HARVEST:
        reasons.extend(harvestability.reasons or (harvestability.decision.value,))
    if not collision_check_passed:
        reasons.append("independent collision validation not supplied")

    safe_candidate = replace(
        candidate,
        collision_free=bool(collision_check_passed and candidate.collision_free),
    )
    safety = validate_action(safe_candidate, SafetyLimits())

    if health.status != SensorStatus.OK or harvestability.decision != HarvestDecision.HARVEST:
        status = "SAFE_HOLD"
    elif safety.decision != SafetyDecision.APPROVE:
        status = "BLOCKED"
    else:
        status = "PROPOSAL_APPROVED_NOT_EXECUTED"

    all_reasons = tuple(dict.fromkeys([*reasons, *safety.reasons]))
    notes = (
        "Synthetic/demo neural outputs are not calibrated harvest evidence.",
        "Trajectory planner and inverse kinematics are prototype implementations.",
        "No ROS 2 or physical actuator command is issued.",
        "A validated robot model, calibrated sensors, independent collision checking, "
        "and human-approved physical safety validation are required before deployment.",
    )
    return EndToEndReport(
        status=status,
        sensor_status=health.status.value,
        sensor_quality=health.quality,
        harvestability_decision=harvestability.decision.value,
        harvestability_score=harvestability.score,
        safety_decision=safety.decision.value,
        safety_reasons=all_reasons,
        perception_summary=result.summary(),
        trajectory_waypoint_count=len(result.trajectory_waypoints),
        trajectory_is_verified=False,
        actuator_commands_sent=False,
        notes=notes,
    )

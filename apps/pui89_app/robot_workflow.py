"""End-to-end task orchestration for Coconut Harvest AI.

This module connects supplied detections/spatial estimates to target selection,
preflight gates, a simulated action sequence, and an audit report. It does not
perform image detection, derive metric 3D position from RGB, or command hardware.
All spatial estimates must come from a separately calibrated/validated source.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from math import isfinite
from typing import Any, Iterable


class WorkflowState(str, Enum):
    IDLE = "IDLE"
    TARGET_SELECTED = "TARGET_SELECTED"
    PLAN_VALIDATED = "PLAN_VALIDATED"
    EXECUTING_SIMULATION = "EXECUTING_SIMULATION"
    COMPLETED_SIMULATION = "COMPLETED_SIMULATION"
    SAFE_HOLD = "SAFE_HOLD"
    FAULT = "FAULT"


@dataclass(frozen=True)
class Candidate:
    target_id: str
    confidence: float
    bbox_xyxy_pixels: tuple[float, float, float, float]
    # Metres in a declared, calibrated robot/world frame; never infer from bbox.
    world_position_m: tuple[float, float, float] | None = None
    localization_uncertainty_m: float | None = None
    track_age_frames: int = 0
    timestamp_s: float = 0.0
    obstacle_clearance_m: float | None = None
    reachable: bool | None = None


@dataclass(frozen=True)
class WorkflowConfig:
    min_detection_confidence: float = 0.50
    max_localization_uncertainty_m: float = 0.10
    min_track_age_frames: int = 3
    max_data_age_s: float = 0.50
    min_obstacle_clearance_m: float = 0.30
    max_reach_m: float = 2.80


@dataclass
class WorkflowReport:
    status: str
    state_history: list[str]
    selected_target_id: str | None
    plan: list[dict[str, Any]]
    rejected_candidates: dict[str, list[str]]
    audit_events: list[dict[str, Any]]
    actuator_commands_sent: bool = False
    physical_harvest_verified: bool = False
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _finite_tuple(values: Iterable[float], expected: int) -> bool:
    values = tuple(values)
    return len(values) == expected and all(isfinite(float(v)) for v in values)


def validate_candidate(candidate: Candidate, *, now_s: float,
                       config: WorkflowConfig = WorkflowConfig()) -> list[str]:
    """Return explicit reasons why a candidate cannot be planned."""
    reasons: list[str] = []
    if not candidate.target_id.strip():
        reasons.append("TARGET_ID_MISSING")
    if not isfinite(candidate.confidence) or not 0 <= candidate.confidence <= 1:
        reasons.append("DETECTION_CONFIDENCE_INVALID")
    elif candidate.confidence < config.min_detection_confidence:
        reasons.append("DETECTION_CONFIDENCE_LOW")
    if not _finite_tuple(candidate.bbox_xyxy_pixels, 4):
        reasons.append("BOUNDING_BOX_INVALID")
    else:
        x1, y1, x2, y2 = candidate.bbox_xyxy_pixels
        if x1 < 0 or y1 < 0 or x2 <= x1 or y2 <= y1:
            reasons.append("BOUNDING_BOX_INVALID")
    if candidate.world_position_m is None:
        reasons.append("METRIC_3D_POSITION_MISSING")
    elif not _finite_tuple(candidate.world_position_m, 3):
        reasons.append("METRIC_3D_POSITION_INVALID")
    else:
        x, y, z = candidate.world_position_m
        if (x * x + y * y + z * z) ** 0.5 > config.max_reach_m:
            reasons.append("OUTSIDE_CONFIGURED_REACH")
    uncertainty = candidate.localization_uncertainty_m
    if uncertainty is None:
        reasons.append("LOCALIZATION_UNCERTAINTY_MISSING")
    elif not isfinite(uncertainty) or uncertainty < 0:
        reasons.append("LOCALIZATION_UNCERTAINTY_INVALID")
    elif uncertainty > config.max_localization_uncertainty_m:
        reasons.append("LOCALIZATION_UNCERTAINTY_TOO_HIGH")
    if candidate.track_age_frames < config.min_track_age_frames:
        reasons.append("TRACK_NOT_STABLE")
    if not isfinite(candidate.timestamp_s) or not isfinite(now_s):
        reasons.append("TIMESTAMP_INVALID")
    elif now_s - candidate.timestamp_s < 0:
        reasons.append("TIMESTAMP_IN_FUTURE")
    elif now_s - candidate.timestamp_s > config.max_data_age_s:
        reasons.append("DATA_STALE")
    clearance = candidate.obstacle_clearance_m
    if clearance is None:
        reasons.append("OBSTACLE_CLEARANCE_MISSING")
    elif not isfinite(clearance) or clearance < 0:
        reasons.append("OBSTACLE_CLEARANCE_INVALID")
    elif clearance < config.min_obstacle_clearance_m:
        reasons.append("OBSTACLE_CLEARANCE_INSUFFICIENT")
    if candidate.reachable is not True:
        reasons.append("REACHABILITY_NOT_CONFIRMED")
    return reasons


def run_simulated_workflow(
    candidates: list[Candidate],
    *,
    now_s: float,
    human_approved: bool = False,
    emergency_stop: bool = False,
    config: WorkflowConfig = WorkflowConfig(),
) -> WorkflowReport:
    """Plan and simulate a single target; never connects to physical actuators."""
    history = [WorkflowState.IDLE.value]
    events: list[dict[str, Any]] = []
    rejected: dict[str, list[str]] = {}
    plan: list[dict[str, Any]] = []

    def event(name: str, **details: Any) -> None:
        events.append({"event": name, **details})

    if emergency_stop:
        history.append(WorkflowState.SAFE_HOLD.value)
        event("SAFE_HOLD", reason="EMERGENCY_STOP_ACTIVE")
        return WorkflowReport(
            status="SAFE_HOLD", state_history=history, selected_target_id=None,
            plan=[], rejected_candidates={}, audit_events=events,
            notes=["Simulation only. No physical actuator command is available."],
        )

    if not candidates:
        history.append(WorkflowState.SAFE_HOLD.value)
        event("SAFE_HOLD", reason="NO_CANDIDATES")
        return WorkflowReport(
            status="SAFE_HOLD", state_history=history, selected_target_id=None,
            plan=[], rejected_candidates={}, audit_events=events,
            notes=["No target was available; the system abstained."],
        )

    eligible: list[Candidate] = []
    for candidate in candidates:
        reasons = validate_candidate(candidate, now_s=now_s, config=config)
        if reasons:
            rejected[candidate.target_id] = reasons
            event("CANDIDATE_REJECTED", target_id=candidate.target_id, reasons=reasons)
        else:
            eligible.append(candidate)

    if not eligible:
        history.append(WorkflowState.SAFE_HOLD.value)
        event("SAFE_HOLD", reason="NO_CANDIDATE_PASSED_GATES")
        return WorkflowReport(
            status="SAFE_HOLD", state_history=history, selected_target_id=None,
            plan=[], rejected_candidates=rejected, audit_events=events,
            notes=["Missing or untrusted evidence causes abstention, not guessed values."],
        )

    # Deterministic, explainable ranking: confidence first, then shorter distance.
    selected = sorted(
        eligible,
        key=lambda c: (
            -c.confidence,
            sum(float(v) ** 2 for v in (c.world_position_m or (0, 0, 0))) ** 0.5,
            c.target_id,
        ),
    )[0]
    history.append(WorkflowState.TARGET_SELECTED.value)
    event("TARGET_SELECTED", target_id=selected.target_id,
          confidence=selected.confidence, ranking="confidence_then_distance")

    if not human_approved:
        history.append(WorkflowState.SAFE_HOLD.value)
        event("SAFE_HOLD", reason="HUMAN_APPROVAL_REQUIRED")
        return WorkflowReport(
            status="AWAITING_HUMAN_APPROVAL", state_history=history,
            selected_target_id=selected.target_id, plan=[], rejected_candidates=rejected,
            audit_events=events,
            notes=["Target selection is not permission to move. No actuator command was sent."],
        )

    position = selected.world_position_m
    assert position is not None  # validated above
    plan = [
        {"step": 1, "action": "APPROACH_PREVIEW", "target_id": selected.target_id,
         "world_position_m": list(position), "execution": "SIMULATED_ONLY"},
        {"step": 2, "action": "HARVEST_TOOL_SEQUENCE_PREVIEW",
         "target_id": selected.target_id, "execution": "SIMULATED_ONLY"},
        {"step": 3, "action": "RETRACT_PREVIEW",
         "target_id": selected.target_id, "execution": "SIMULATED_ONLY"},
    ]
    history.append(WorkflowState.PLAN_VALIDATED.value)
    event("PLAN_VALIDATED", step_count=len(plan),
          validation="configured preflight gates only; no independent physics/collision proof")
    history.append(WorkflowState.EXECUTING_SIMULATION.value)
    for step in plan:
        event("SIMULATED_STEP", **step)
    history.append(WorkflowState.COMPLETED_SIMULATION.value)
    event("SIMULATION_COMPLETED", target_id=selected.target_id,
          physical_result="NOT_OBSERVED")
    return WorkflowReport(
        status="COMPLETED_SIMULATION", state_history=history,
        selected_target_id=selected.target_id, plan=plan,
        rejected_candidates=rejected, audit_events=events,
        notes=[
            "This is a software task-sequence simulation, not physics simulation.",
            "No ROS 2, motor, gripper, or cutter command was sent.",
            "Physical harvest success is not observed or claimed.",
            "Collision-free motion still requires a robot model and independent simulator/checker.",
        ],
    )

"""Local, deterministic harvest-planning agent for Coconut Harvest AI.

This is a decision-support prototype. It does not run a detector, estimate depth,
plan robot kinematics, or send actuator commands. Inputs are supplied by a caller.
Only standard-library modules are required.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


COCONUT_STAGES = {
    "flower_or_infant",
    "young_green",
    "mature_green",
    "mature_brown_or_dry",
    "damaged_or_abnormal",
    "occluded_or_partial",
    "uncertain_stage",
}

HARVEST_MODES = {
    "young_green": {"young_green"},
    "mature_green": {"mature_green"},
    "mature_brown_or_dry": {"mature_brown_or_dry"},
    "all_mature": {"mature_green", "mature_brown_or_dry"},
    "survey_only": set(),
}


@dataclass(frozen=True)
class CoconutCandidate:
    """Candidate target supplied by a detector or entered for a demo."""

    target_id: str
    confidence: float
    x_m: float | None = None
    y_m: float | None = None
    z_m: float | None = None
    reachable: bool | None = None
    occluded: bool = False
    # This is an upstream/manual label, not a maturity prediction by this agent.
    stage: str = "uncertain_stage"


@dataclass(frozen=True)
class AgentConfig:
    min_confidence: float = 0.60
    max_range_m: float = 3.0
    min_range_m: float = 0.15
    require_3d_position: bool = True


@dataclass(frozen=True)
class CandidateAssessment:
    target_id: str
    status: str
    reasons: tuple[str, ...]
    distance_m: float | None
    confidence: float
    stage: str


def assess_candidate(
    candidate: CoconutCandidate,
    config: AgentConfig = AgentConfig(),
    selected_stages: set[str] | None = None,
    survey_only: bool = False,
) -> CandidateAssessment:
    """Apply conservative checks and, when requested, operator stage filtering."""
    reasons: list[str] = []
    coords = (candidate.x_m, candidate.y_m, candidate.z_m)
    distance: float | None = None

    if not 0.0 <= candidate.confidence <= 1.0:
        reasons.append("confidence must be between 0 and 1")
    elif candidate.confidence < config.min_confidence:
        reasons.append("confidence below configured threshold")

    if candidate.occluded:
        reasons.append("target is marked occluded")

    if selected_stages is not None:
        if candidate.stage not in COCONUT_STAGES:
            reasons.append("stage label is invalid; request human review")
        elif candidate.stage in {"uncertain_stage", "occluded_or_partial", "damaged_or_abnormal", "flower_or_infant"}:
            reasons.append("stage is not eligible for automatic harvest; human review required")
        elif candidate.stage not in selected_stages:
            reasons.append("stage does not match the operator's selected harvest mode")

    if survey_only:
        reasons.append("survey-only mode does not authorize harvest selection")

    if any(value is None for value in coords):
        if config.require_3d_position:
            reasons.append("3D position missing; do not plan approach")
    else:
        x, y, z = (float(value) for value in coords)
        distance = (x * x + y * y + z * z) ** 0.5
        if distance < config.min_range_m:
            reasons.append("target is inside minimum range")
        if distance > config.max_range_m:
            reasons.append("target is outside configured range")

    if candidate.reachable is not True:
        reasons.append("reachability has not been confirmed")

    status = "ELIGIBLE_FOR_SIMULATION_REVIEW" if not reasons else "REJECTED"
    return CandidateAssessment(
        target_id=candidate.target_id,
        status=status,
        reasons=tuple(reasons),
        distance_m=round(distance, 4) if distance is not None else None,
        confidence=candidate.confidence,
        stage=candidate.stage,
    )


def propose_plan(
    candidates: Iterable[CoconutCandidate],
    config: AgentConfig = AgentConfig(),
    harvest_mode: str | None = None,
    selected_stages: Iterable[str] | None = None,
) -> dict[str, Any]:
    """Rank candidates for simulation review; never return an execution command.

    If harvest_mode is omitted, legacy stage-agnostic demo behaviour is retained.
    For selected_combination, selected_stages must explicitly list the requested
    eligible stages. Labels are supplied evidence, not predictions by this agent.
    """
    allowed_modes = set(HARVEST_MODES) | {"selected_combination"}
    if harvest_mode is not None and harvest_mode not in allowed_modes:
        raise ValueError(f"Unknown harvest_mode: {harvest_mode}")

    stage_filter: set[str] | None = None
    survey_only = harvest_mode == "survey_only"
    if harvest_mode in HARVEST_MODES:
        stage_filter = set(HARVEST_MODES[harvest_mode])
    elif harvest_mode == "selected_combination":
        if selected_stages is None:
            raise ValueError("selected_stages is required for selected_combination")
        stage_filter = set(selected_stages)
        if not stage_filter or not stage_filter <= COCONUT_STAGES:
            raise ValueError("selected_stages must contain valid coconut stage labels")
        if stage_filter & {"flower_or_infant", "damaged_or_abnormal", "occluded_or_partial", "uncertain_stage"}:
            raise ValueError("selected_stages cannot enable uncertain, damaged, occluded, or infant targets for automatic harvest")

    assessments = [
        assess_candidate(item, config, stage_filter, survey_only)
        for item in candidates
    ]
    by_id = {item.target_id: item for item in assessments}
    eligible = [
        item for item in assessments if item.status == "ELIGIBLE_FOR_SIMULATION_REVIEW"
    ]
    eligible.sort(
        key=lambda item: (
            -item.confidence,
            item.distance_m if item.distance_m is not None else float("inf"),
            item.target_id,
        )
    )
    return {
        "agent": "coconut-harvest-rule-agent",
        "status": "PROPOSAL_ONLY" if eligible else "SAFE_HOLD",
        "harvest_mode": harvest_mode or "legacy_unfiltered_demo",
        "selected_stages": sorted(stage_filter) if stage_filter is not None else None,
        "recommended_target_id": eligible[0].target_id if eligible else None,
        "eligible_target_ids": [item.target_id for item in eligible],
        "assessments": [asdict(by_id[key]) for key in sorted(by_id)],
        "safety_boundary": {
            "actuator_commands_sent": False,
            "physical_robot_authorized": False,
            "independent_collision_check_required": True,
            "human_review_required": True,
        },
        "limitations": [
            "Candidate detections, stage labels and positions are supplied inputs, not predictions produced by this agent.",
            "Colour alone does not establish physiological maturity; class criteria require grower review.",
            "Reachability must be supplied by a validated robot-specific checker.",
            "This rule agent does not detect coconuts or validate collision-free motion.",
            "Eligible means eligible for simulation review only, not safe to harvest.",
        ],
    }


def load_candidates(path: Path) -> list[CoconutCandidate]:
    """Load a JSON list of candidate dictionaries."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("Input JSON must be a list of candidate objects.")
    return [CoconutCandidate(**item) for item in raw]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        help="JSON file containing candidate objects; omit to run the labelled example.",
    )
    parser.add_argument("--output", type=Path, help="Optional path for the JSON report.")
    parser.add_argument(
        "--harvest-mode",
        choices=sorted(set(HARVEST_MODES) | {"selected_combination"}),
        help="Optional operator-selected stage filter. Without this, legacy demo mode is used.",
    )
    parser.add_argument(
        "--selected-stage",
        action="append",
        choices=sorted(COCONUT_STAGES),
        help="Stage to include; repeat for a selected_combination.",
    )
    args = parser.parse_args()

    if args.input:
        candidates = load_candidates(args.input)
    else:
        # Synthetic demonstration data only; not detections from a real camera.
        candidates = [
            CoconutCandidate("demo-young", 0.91, 1.2, 0.2, 1.1, reachable=True, stage="young_green"),
            CoconutCandidate("demo-mature-green", 0.90, 1.5, 0.0, 1.0, reachable=True, stage="mature_green"),
            CoconutCandidate("demo-mature-brown", 0.95, 1.4, 0.0, 1.0, reachable=True, stage="mature_brown_or_dry"),
            CoconutCandidate("demo-uncertain", 0.99, 1.0, 0.1, 1.0, reachable=True, stage="uncertain_stage"),
        ]

    report = propose_plan(
        candidates,
        harvest_mode=args.harvest_mode,
        selected_stages=args.selected_stage,
    )
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

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


@dataclass(frozen=True)
class CoconutCandidate:
    """Candidate target produced by a detector or entered for a demo."""

    target_id: str
    confidence: float
    x_m: float | None = None
    y_m: float | None = None
    z_m: float | None = None
    reachable: bool | None = None
    occluded: bool = False


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


def assess_candidate(
    candidate: CoconutCandidate, config: AgentConfig = AgentConfig()
) -> CandidateAssessment:
    """Apply conservative, explicit checks to one candidate."""
    reasons: list[str] = []
    coords = (candidate.x_m, candidate.y_m, candidate.z_m)
    distance: float | None = None

    if not 0.0 <= candidate.confidence <= 1.0:
        reasons.append("confidence must be between 0 and 1")
    elif candidate.confidence < config.min_confidence:
        reasons.append("confidence below configured threshold")

    if candidate.occluded:
        reasons.append("target is marked occluded")

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
    )


def propose_plan(
    candidates: Iterable[CoconutCandidate],
    config: AgentConfig = AgentConfig(),
) -> dict[str, Any]:
    """Rank eligible candidates and return a proposal, never an execution command."""
    assessments = [assess_candidate(item, config) for item in candidates]
    by_id = {item.target_id: item for item in assessments}
    eligible = [
        item for item in assessments if item.status == "ELIGIBLE_FOR_SIMULATION_REVIEW"
    ]
    # Prefer higher confidence; break ties by nearer target and then stable ID.
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
            "Candidate detections and positions are inputs, not produced by this agent.",
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
    args = parser.parse_args()

    if args.input:
        candidates = load_candidates(args.input)
    else:
        # Synthetic demonstration data only; not detections from a real camera.
        candidates = [
            CoconutCandidate("demo-A", 0.91, 1.2, 0.2, 1.1, reachable=True),
            CoconutCandidate("demo-B", 0.54, 1.0, 0.1, 1.0, reachable=True),
            CoconutCandidate("demo-C", 0.88, 4.0, 0.0, 0.5, reachable=True),
            CoconutCandidate("demo-D", 0.95, 1.4, 0.0, 1.0, reachable=None),
        ]

    report = propose_plan(candidates)
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

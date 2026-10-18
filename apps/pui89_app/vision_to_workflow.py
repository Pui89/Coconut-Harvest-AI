"""Bridge local RGB-D proposals into a conservative simulation-only robot workflow.

Camera-frame points are never treated as robot-base points without an explicit,
validated 4x4 camera-to-robot-base transform. Missing robot evidence fails closed.
No hardware drivers or actuator commands exist in this module.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from apps.pui89_app.robot_workflow import Candidate, run_simulated_workflow


def _finite_number(value: Any, name: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def _validated_transform(value: Any) -> list[list[float]] | None:
    if value is None:
        return None
    if not isinstance(value, list) or len(value) != 4:
        raise ValueError("camera_to_robot_base_4x4 must be a 4x4 list")
    matrix = []
    for row in value:
        if not isinstance(row, list) or len(row) != 4:
            raise ValueError("camera_to_robot_base_4x4 must be a 4x4 list")
        matrix.append([_finite_number(v, "transform value") for v in row])
    if any(abs(a - b) > 1e-6 for a, b in zip(matrix[3], [0.0, 0.0, 0.0, 1.0])):
        raise ValueError("transform last row must be [0, 0, 0, 1]")
    rotation = [row[:3] for row in matrix[:3]]
    for i in range(3):
        for j in range(3):
            dot = sum(rotation[i][k] * rotation[j][k] for k in range(3))
            expected = 1.0 if i == j else 0.0
            if abs(dot - expected) > 1e-3:
                raise ValueError("transform rotation must be orthonormal")
    r = rotation
    determinant = (
        r[0][0] * (r[1][1] * r[2][2] - r[1][2] * r[2][1])
        - r[0][1] * (r[1][0] * r[2][2] - r[1][2] * r[2][0])
        + r[0][2] * (r[1][0] * r[2][1] - r[1][1] * r[2][0])
    )
    if abs(determinant - 1.0) > 1e-3:
        raise ValueError("transform rotation must have determinant +1")
    return matrix


def transform_camera_point(point: tuple[float, float, float], matrix: list[list[float]]) -> tuple[float, float, float]:
    """Apply a supplied homogeneous camera-to-robot-base transform in metres."""
    if len(point) != 3 or not all(math.isfinite(float(v)) for v in point):
        raise ValueError("camera-frame point must contain three finite coordinates")
    homogeneous = [float(point[0]), float(point[1]), float(point[2]), 1.0]
    out = [sum(matrix[r][c] * homogeneous[c] for c in range(4)) for r in range(4)]
    if not all(math.isfinite(v) for v in out) or abs(out[3]) < 1e-9:
        raise ValueError("transform produced invalid homogeneous coordinates")
    return tuple(v / out[3] for v in out[:3])


def proposal_to_candidates(proposal: dict[str, Any], evidence: dict[str, Any]) -> tuple[list[Candidate], dict[str, list[str]]]:
    """Convert only the local proposal schema; missing calibration/evidence stays missing."""
    if proposal.get("mode") != "LOCAL_ONLY_PROPOSAL":
        raise ValueError("proposal mode must be LOCAL_ONLY_PROPOSAL")
    if proposal.get("actuator_commands_authorized") is not False:
        raise ValueError("proposal must explicitly forbid actuator commands")

    now_s = _finite_number(evidence.get("now_s"), "evidence.now_s")
    transform = _validated_transform(evidence.get("camera_to_robot_base_4x4"))
    evidence_by_target = evidence.get("evidence_by_target", {})
    if not isinstance(evidence_by_target, dict):
        raise ValueError("evidence_by_target must be an object")

    candidates: list[Candidate] = []
    upstream_rejected: dict[str, list[str]] = {}
    for item in proposal.get("candidates", []):
        target_id = str(item.get("target_id", "")).strip()
        if item.get("status") == "REJECTED":
            upstream_rejected[target_id or "unnamed-target"] = list(item.get("reasons", ["UPSTREAM_REJECTED"]))
            continue
        if item.get("status") not in {"REVIEW_REQUIRED", "HUMAN_APPROVED_PROPOSAL_ONLY"}:
            upstream_rejected[target_id or "unnamed-target"] = ["UPSTREAM_STATUS_NOT_ELIGIBLE"]
            continue

        bbox_raw = item.get("box_xyxy", ())
        try:
            bbox = tuple(float(v) for v in bbox_raw)
            if len(bbox) != 4:
                raise ValueError
        except (TypeError, ValueError):
            bbox = (0.0, 0.0, 0.0, 0.0)

        localization = item.get("localization", {})
        world_position = None
        if transform is not None and localization.get("status") == "ESTIMATED_CAMERA_FRAME":
            try:
                camera_point = tuple(float(localization[k]) for k in ("x_m", "y_m", "z_m"))
                world_position = transform_camera_point(camera_point, transform)
            except (KeyError, TypeError, ValueError, OverflowError):
                world_position = None

        ext = evidence_by_target.get(target_id, {})
        if not isinstance(ext, dict):
            ext = {}
        try:
            confidence = float(item.get("confidence", math.nan))
        except (TypeError, ValueError):
            confidence = math.nan
        try:
            uncertainty = float(ext["localization_uncertainty_m"]) if ext.get("localization_uncertainty_m") is not None else None
        except (TypeError, ValueError):
            uncertainty = math.nan
        try:
            track_age = int(ext.get("track_age_frames", 0))
        except (TypeError, ValueError):
            track_age = 0
        try:
            timestamp = float(ext["timestamp_s"]) if ext.get("timestamp_s") is not None else math.nan
        except (TypeError, ValueError):
            timestamp = math.nan
        try:
            clearance = float(ext["obstacle_clearance_m"]) if ext.get("obstacle_clearance_m") is not None else None
        except (TypeError, ValueError):
            clearance = math.nan
        reachable = ext.get("reachable")
        if not isinstance(reachable, bool):
            reachable = None

        candidates.append(Candidate(
            target_id=target_id,
            confidence=confidence,
            bbox_xyxy_pixels=bbox,  # type: ignore[arg-type]
            world_position_m=world_position,
            localization_uncertainty_m=uncertainty,
            track_age_frames=track_age,
            timestamp_s=timestamp,
            obstacle_clearance_m=clearance,
            reachable=reachable,
        ))
    return candidates, upstream_rejected


def run_vision_to_simulated_workflow(
    proposal: dict[str, Any], evidence: dict[str, Any], *,
    human_approved: bool = False, emergency_stop: bool = False,
) -> dict[str, Any]:
    candidates, upstream_rejected = proposal_to_candidates(proposal, evidence)
    now_s = float(evidence["now_s"])
    report = run_simulated_workflow(
        candidates, now_s=now_s, human_approved=human_approved, emergency_stop=emergency_stop
    ).to_dict()
    return {
        "schema_version": "1.0",
        "mode": "SIMULATION_ONLY",
        "upstream_rejected_candidates": upstream_rejected,
        "workflow_report": report,
        "actuator_commands_sent": False,
        "physical_harvest_verified": False,
        "limitations": [
            "Robot-base coordinates require a validated camera-to-robot-base transform.",
            "Reachability and obstacle-clearance fields must come from validated robot/sensor evidence.",
            "This workflow simulates task decisions only and does not control hardware.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proposal", required=True, help="JSON produced by local_first_pipeline.py")
    parser.add_argument("--evidence", required=True, help="Robot-frame transform and per-target evidence JSON")
    parser.add_argument("--output", default="coconut_simulated_workflow_report.json")
    parser.add_argument("--human-approved", action="store_true", help="Explicitly approve simulation planning only")
    parser.add_argument("--emergency-stop", action="store_true", help="Force a safe hold in simulation")
    args = parser.parse_args(argv)

    proposal = json.loads(Path(args.proposal).read_text(encoding="utf-8"))
    evidence = json.loads(Path(args.evidence).read_text(encoding="utf-8"))
    report = run_vision_to_simulated_workflow(
        proposal, evidence, human_approved=args.human_approved, emergency_stop=args.emergency_stop
    )
    Path(args.output).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({
        "output": args.output,
        "workflow_status": report["workflow_report"]["status"],
        "selected_target_id": report["workflow_report"]["selected_target_id"],
        "actuator_commands_sent": False,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

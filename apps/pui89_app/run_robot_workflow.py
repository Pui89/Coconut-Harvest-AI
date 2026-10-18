"""Run a sample end-to-end, simulation-only workflow from JSON input.

Usage:
  python -m apps.pui89_app.run_robot_workflow
  python -m apps.pui89_app.run_robot_workflow --input examples/end_to_end_robot_workflow.example.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    from apps.pui89_app.robot_workflow import Candidate, run_simulated_workflow
except ModuleNotFoundError:  # Support direct invocation from the repository root.
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from apps.pui89_app.robot_workflow import Candidate, run_simulated_workflow


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="examples/end_to_end_robot_workflow.example.json")
    parser.add_argument("--output", help="Optional path for the JSON audit report.")
    parser.add_argument("--require-human-approval", action="store_true",
                        help="Ignore input approval and require explicit CLI approval.")
    args = parser.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    candidates = [Candidate(
        target_id=item["target_id"],
        confidence=item["confidence"],
        bbox_xyxy_pixels=tuple(item["bbox_xyxy_pixels"]),
        world_position_m=tuple(item["world_position_m"]) if item.get("world_position_m") is not None else None,
        localization_uncertainty_m=item.get("localization_uncertainty_m"),
        track_age_frames=item.get("track_age_frames", 0),
        timestamp_s=item.get("timestamp_s", 0.0),
        obstacle_clearance_m=item.get("obstacle_clearance_m"),
        reachable=item.get("reachable"),
    ) for item in payload.get("candidates", [])]
    approved = bool(payload.get("human_approved", False))
    if args.require_human_approval:
        approved = False
        print("Human approval required. Review the proposed target, then rerun only in this simulation demo.", file=sys.stderr)
    report = run_simulated_workflow(
        candidates,
        now_s=float(payload.get("now_s", 0.0)),
        human_approved=approved,
        emergency_stop=bool(payload.get("emergency_stop", False)),
    ).to_dict()
    rendered = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

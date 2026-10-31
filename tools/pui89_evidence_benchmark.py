#!/usr/bin/env python3
"""Build a deterministic, standard-library PUI89 evidence benchmark from simulation reports.

This summarizes rule-based scenario evidence. It deliberately does not rank unlike
projects or compare observed latency across different hosts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path
from typing import Any

ENGINE_VERSION = "pui89-evidence-benchmark-1.0.0"


def stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def summarize(report_path: Path) -> dict[str, Any]:
    raw = report_path.read_bytes()
    report = json.loads(raw.decode("utf-8"))
    required = ("schema_version", "project_id", "run_id", "scenario_config_sha256",
                "status", "metrics", "scenarios", "steps", "failures")
    missing = [key for key in required if key not in report]
    if missing:
        raise ValueError(f"{report_path}: missing fields: {', '.join(missing)}")
    if report["schema_version"] != 1:
        raise ValueError(f"{report_path}: unsupported report schema")
    metrics, steps, scenarios, failures = report["metrics"], report["steps"], report["scenarios"], report["failures"]
    if not isinstance(metrics, dict) or not all(isinstance(value, list) for value in (steps, scenarios, failures)):
        raise ValueError(f"{report_path}: invalid metrics/scenarios/steps/failures types")
    if metrics.get("step_count") != len(steps) or metrics.get("scenario_count") != len(scenarios):
        raise ValueError(f"{report_path}: scenario/step counts do not match rows")
    if metrics.get("failure_count") != len(failures):
        raise ValueError(f"{report_path}: failure_count does not match failure rows")
    passed_steps = sum(row.get("passed") is True for row in steps)
    passed_scenarios = sum(row.get("passed") is True for row in scenarios)
    if metrics.get("step_pass_count") != passed_steps or metrics.get("scenario_pass_count") != passed_scenarios:
        raise ValueError(f"{report_path}: pass counts do not match rows")
    if any(not isinstance(row, dict) or row.get("hardware_actuation") is not False for row in steps):
        raise ValueError(f"{report_path}: hardware_actuation must be explicitly false on every step")
    if report["status"] not in ("PASS", "FAIL") or ((report["status"] == "PASS") != (len(failures) == 0)):
        raise ValueError(f"{report_path}: status conflicts with failure rows")
    world_states = [sha256_bytes(stable_json(row.get("state", {})).encode("utf-8")) for row in steps]
    return {
        "project_id": report["project_id"], "run_id": report["run_id"], "status": report["status"],
        "scenario_config_sha256": report["scenario_config_sha256"],
        "source_report_sha256": sha256_bytes(raw),
        "scenario_count": len(scenarios), "scenario_pass_count": passed_scenarios,
        "step_count": len(steps), "step_pass_count": passed_steps, "failure_count": len(failures),
        "step_pass_rate": metrics.get("step_pass_rate"), "scenario_pass_rate": metrics.get("scenario_pass_rate"),
        "safe_hold_count": metrics.get("safe_hold_count"),
        "world_state_snapshot_count": len(world_states),
        "world_state_sequence_sha256": sha256_bytes(stable_json(world_states).encode("utf-8")),
        "hardware_actuation": False,
        "limitations": [
            "Rule-based simulation evidence only; not a real AI model benchmark.",
            "Different project scenarios are not directly comparable or ranked.",
            "Observed timing is excluded from cross-run comparisons.",
            "No physical robot, field, sensor, detector, or operational validation is implied."
        ]
    }


def build(report_paths: list[Path]) -> dict[str, Any]:
    if not report_paths:
        raise ValueError("at least one --report path is required")
    items = [summarize(path) for path in report_paths]
    project_ids = [item["project_id"] for item in items]
    if len(project_ids) != len(set(project_ids)):
        raise ValueError("duplicate project_id values; provide one report per project")
    return {
        "schema_version": 1, "benchmark_engine": ENGINE_VERSION,
        "benchmark_type": "evidence_integrity_summary_not_cross_project_performance_ranking",
        "runtime_environment": {"python": platform.python_version(),
                                "implementation": platform.python_implementation(),
                                "platform": platform.platform()},
        "project_count": len(items), "all_reports_integrity_valid": True,
        "all_hardware_actuation_false": all(item["hardware_actuation"] is False for item in items),
        "projects": sorted(items, key=lambda item: item["project_id"]),
        "comparison_policy": "Compare a project only against its own compatible scenario/configuration and engine version. Never rank different project scenarios by pass rate."
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, action="append", required=True,
                        help="Simulation JSON report; repeat once per project.")
    parser.add_argument("--output", type=Path, default=Path("reports/pui89-evidence-benchmark.json"))
    args = parser.parse_args()
    try:
        result = build(args.report)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"benchmark={ENGINE_VERSION} projects={result['project_count']} integrity_valid=true "
              f"hardware_actuation=false output={args.output}")
        return 0
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError, TypeError) as exc:
        print(f"EVIDENCE_BENCHMARK_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

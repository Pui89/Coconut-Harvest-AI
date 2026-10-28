#!/usr/bin/env python3
"""Validate PUI89 simulation evidence files using only the Python standard library."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path


def stable_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def validate(report_path: Path, config_path: Path) -> list[str]:
    errors = []
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read report/config JSON: {exc}"]
    required = ("schema_version", "project_id", "run_id", "scenario_config_sha256",
                "status", "metrics", "scenarios", "steps", "failures", "output_files")
    for key in required:
        if key not in report:
            errors.append(f"missing report field: {key}")
    if errors:
        return errors
    if report["schema_version"] != 1:
        errors.append("unsupported report schema_version")
    if report["project_id"] != config.get("project_id"):
        errors.append("project_id does not match scenario config")
    expected_hash = hashlib.sha256(stable_json(config).encode("utf-8")).hexdigest()
    if report["scenario_config_sha256"] != expected_hash:
        errors.append("scenario config SHA-256 mismatch")
    if not re.fullmatch(r"[0-9a-f]{64}", str(report["scenario_config_sha256"])):
        errors.append("scenario_config_sha256 is not a 64-character lowercase SHA-256")
    metrics = report["metrics"]
    for key in ("scenario_count", "scenario_pass_count", "step_count",
                "step_pass_count", "failure_count", "step_pass_rate",
                "scenario_pass_rate", "action_counts", "safe_hold_count"):
        if key not in metrics:
            errors.append(f"missing metrics field: {key}")
    if errors:
        return errors
    if metrics["scenario_count"] != len(report["scenarios"]):
        errors.append("scenario_count does not match scenario rows")
    if metrics["step_count"] != len(report["steps"]):
        errors.append("step_count does not match step rows")
    if metrics["failure_count"] != len(report["failures"]):
        errors.append("failure_count does not match failure rows")
    actual_passed_steps = sum(1 for row in report["steps"] if row.get("passed") is True)
    actual_passed_scenarios = sum(1 for row in report["scenarios"] if row.get("passed") is True)
    if metrics["step_pass_count"] != actual_passed_steps:
        errors.append("step_pass_count does not match step rows")
    if metrics["scenario_pass_count"] != actual_passed_scenarios:
        errors.append("scenario_pass_count does not match scenario rows")
    if metrics["step_count"] and abs(metrics["step_pass_rate"] - actual_passed_steps / metrics["step_count"]) > 1e-6:
        errors.append("step_pass_rate is inconsistent")
    if metrics["scenario_count"] and abs(metrics["scenario_pass_rate"] - actual_passed_scenarios / metrics["scenario_count"]) > 1e-6:
        errors.append("scenario_pass_rate is inconsistent")
    expected_status = "PASS" if metrics["failure_count"] == 0 else "FAIL"
    if report["status"] != expected_status:
        errors.append("report status conflicts with failure_count")
    if any(row.get("hardware_actuation") is True for row in report["steps"]):
        errors.append("hardware_actuation must remain false in simulation evidence")
    csv_path = Path(report["output_files"].get("csv", ""))
    if not csv_path.is_file():
        errors.append(f"CSV evidence file not found: {csv_path}")
    else:
        try:
            with csv_path.open(newline="", encoding="utf-8") as stream:
                rows = list(csv.DictReader(stream))
            if len(rows) != metrics["step_count"]:
                errors.append("CSV row count does not match step_count")
            if rows and any(row.get("hardware_actuation", "").lower() == "true" for row in rows):
                errors.append("CSV evidence contains hardware_actuation=true")
        except (OSError, csv.Error) as exc:
            errors.append(f"cannot read CSV evidence: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True,
                        help="JSON report produced by pui89_autonomy_lab.py simulate")
    parser.add_argument("--config", type=Path, default=Path("simulation/scenarios.json"))
    args = parser.parse_args()
    errors = validate(args.report, args.config)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    report = json.loads(args.report.read_text(encoding="utf-8"))
    metrics = report["metrics"]
    print(f"VALID report project={report['project_id']} run_id={report['run_id']} "
          f"scenarios={metrics['scenario_pass_count']}/{metrics['scenario_count']} "
          f"steps={metrics['step_pass_count']}/{metrics['step_count']} "
          f"failures={metrics['failure_count']} hardware_actuation=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

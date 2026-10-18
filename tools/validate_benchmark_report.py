#!/usr/bin/env python3
"""Validate benchmark metadata before results are published.

This standard-library-only gate checks report completeness, not model quality.
It must never be interpreted as evidence that a robot is safe or accurate.
"""
from __future__ import annotations

import argparse
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

REQUIRED_TOP_LEVEL = {
    "schema_version", "project", "run_id", "run_date_utc", "dataset",
    "model", "hardware", "software", "config", "metrics",
}
PLACEHOLDER_TOKENS = ("todo", "tbd", "placeholder", "fill me", "example value")


def _walk_strings(value: Any, path: str = "$"):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _walk_strings(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_strings(child, f"{path}[{index}]")
    elif isinstance(value, str):
        yield path, value


def validate_report(report: Any) -> list[str]:
    """Return human-readable validation errors; an empty list means metadata passes."""
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["$ must contain a JSON object"]
    missing = sorted(REQUIRED_TOP_LEVEL - report.keys())
    if missing:
        errors.append(f"Missing required fields: {', '.join(missing)}")
    for path, value in _walk_strings(report):
        if any(token in value.strip().lower() for token in PLACEHOLDER_TOKENS):
            errors.append(f"{path} contains placeholder text")
    if errors:
        return errors
    if report["schema_version"] != "1.0":
        errors.append("$.schema_version must be '1.0'")
    for field in ("project", "run_id"):
        if not isinstance(report[field], str) or not report[field].strip():
            errors.append(f"$.{field} must be a non-empty string")
    try:
        timestamp = datetime.fromisoformat(str(report["run_date_utc"]).replace("Z", "+00:00"))
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            errors.append("$.run_date_utc must include a timezone (UTC recommended)")
    except (TypeError, ValueError):
        errors.append("$.run_date_utc must be an ISO-8601 timestamp")
    for section, keys in {
        "dataset": ("name", "version", "split"),
        "model": ("name", "version"),
        "hardware": ("platform",),
        "software": ("os", "python"),
        "config": ("seed",),
    }.items():
        value = report[section]
        if not isinstance(value, dict):
            errors.append(f"$.{section} must be an object")
            continue
        for key in keys:
            if key not in value or value[key] in ("", None):
                errors.append(f"$.{section}.{key} is required")
    metrics = report["metrics"]
    if not isinstance(metrics, dict) or not metrics:
        errors.append("$.metrics must be a non-empty object")
    else:
        numeric_leaves = 0
        def check_metric(value: Any, path: str) -> None:
            nonlocal numeric_leaves
            if isinstance(value, dict) and value:
                for key, child in value.items():
                    check_metric(child, f"{path}.{key}")
            elif isinstance(value, (int, float)) and not isinstance(value, bool):
                if not math.isfinite(float(value)):
                    errors.append(f"{path} must be finite")
                numeric_leaves += 1
            else:
                errors.append(f"{path} must be a numeric metric or a non-empty metric group")
        for key, value in metrics.items():
            check_metric(value, f"$.metrics.{key}")
        if numeric_leaves == 0:
            errors.append("$.metrics must contain at least one numeric result")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="Path to a benchmark report JSON file")
    args = parser.parse_args()
    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INVALID: cannot read JSON report: {exc}")
        return 2
    errors = validate_report(report)
    if errors:
        print("INVALID benchmark report:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: benchmark metadata is complete and structurally valid.")
    print("NOTE: this gate does not validate scientific correctness, dataset quality, or robot safety.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

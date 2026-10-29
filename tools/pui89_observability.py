#!/usr/bin/env python3
"""Generate a dependency-free PUI89 observability baseline.

This tool does not inspect hardware, read sensors, load models, call networks,
or control actuators. Without supplied evidence, checks remain NOT_RUN or
NOT_CONNECTED; it never upgrades an unobserved component to PASS.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_STATUS = {"PASS", "FAIL", "NOT_RUN", "NOT_CONNECTED", "UNKNOWN", "BLOCKED"}
REQUIRED_LAYERS = {
    "software": "Code, test and dependency checks",
    "hardware": "Physical devices and sensors",
    "system": "Runtime resources and process health",
    "model": "Model identity, licence, inference and uncertainty",
    "workflow_step": "Ordered pipeline stages and hand-offs",
    "safety_review": "Safe-hold and authorised human-review evidence",
}

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

def baseline() -> dict:
    layers = {}
    for key, description in REQUIRED_LAYERS.items():
        layers[key] = {
            "description": description,
            "status": "NOT_CONNECTED" if key == "hardware" else "NOT_RUN",
            "observed_at": None,
            "evidence_ref": None,
            "detail": "No runtime evidence supplied; status is intentionally not asserted.",
        }
    return {
        "schema_version": "1.0",
        "project": ROOT.name,
        "generated_at": utc_now(),
        "evidence_mode": "baseline_no_live_observation",
        "layers": layers,
        "limitations": [
            "This report does not inspect the host system, sensors, hardware, or model runtime.",
            "No model accuracy, physical safety, or field performance is established.",
            "Synthetic and software-only checks do not validate real-world performance.",
        ],
    }

def validate(data: object) -> list[str]:
    errors = []
    if not isinstance(data, dict) or not isinstance(data.get("layers"), dict):
        return ["top-level JSON must contain a layers object"]
    layers = data["layers"]
    for key, record in layers.items():
        if key not in REQUIRED_LAYERS:
            errors.append(f"unknown layer: {key}")
            continue
        if not isinstance(record, dict):
            errors.append(f"{key}: record must be an object")
            continue
        status = record.get("status")
        if status not in ALLOWED_STATUS:
            errors.append(f"{key}: invalid status {status!r}")
            continue
        if status in {"PASS", "FAIL"}:
            if not isinstance(record.get("evidence_ref"), str) or not record["evidence_ref"].strip():
                errors.append(f"{key}: {status} requires a non-empty evidence_ref")
            if not isinstance(record.get("observed_at"), str) or not record["observed_at"].strip():
                errors.append(f"{key}: {status} requires observed_at")
    missing = set(REQUIRED_LAYERS) - set(layers)
    if missing:
        errors.append("missing required layers: " + ", ".join(sorted(missing)))
    return errors

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, help="optional JSON evidence file to validate and include")
    parser.add_argument("--report", type=Path, default=Path("observability-report.json"), help="output JSON report path")
    args = parser.parse_args()
    report = baseline()
    if args.evidence:
        try:
            supplied = json.loads(args.evidence.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"Could not read evidence JSON: {exc}", file=sys.stderr)
            return 2
        errors = validate(supplied)
        if errors:
            print("Evidence validation failed:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 2
        report["evidence_mode"] = "user_supplied_evidence_validated_for_schema_only"
        report["layers"] = supplied["layers"]
        report["evidence_validation_note"] = "Schema validation does not verify that evidence is genuine."
    try:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except OSError as exc:
        print(f"Could not write report: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({
        "report": str(args.report),
        "evidence_mode": report["evidence_mode"],
        "statuses": {key: value["status"] for key, value in report["layers"].items()},
        "note": "No live hardware/system/model observation was performed by this tool."
    }, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

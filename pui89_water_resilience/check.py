#!/usr/bin/env python3
"""PUI89 water-resilience software contract checks; standard library only."""
from __future__ import annotations
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / ".pui89" / "water_resilience.json"

def classify(*, sensor_valid: bool, ingress_detected: bool, temperature_c: float, temperature_limit_c: float) -> str:
    # Invalid/missing evidence must fail safe before evaluating a normal state.
    if not sensor_valid:
        return "SENSOR_FAULT_SAFE_HOLD"
    if ingress_detected:
        return "CRITICAL_INGRESS_STOP"
    if temperature_c >= temperature_limit_c:
        return "THERMAL_WARNING"
    return "NORMAL_MONITORING"

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args()
    if not CONFIG.exists():
        print(f"FAIL: missing configuration: {CONFIG}", file=sys.stderr)
        return 2
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    required = {"project", "exposure", "sensors", "temperature_limit_c", "physical_validation"}
    missing = sorted(required - config.keys())
    if missing:
        print("FAIL: missing config keys: " + ", ".join(missing), file=sys.stderr)
        return 2
    if not isinstance(config["sensors"], list) or not config["sensors"]:
        print("FAIL: sensors must be a non-empty list", file=sys.stderr)
        return 2
    if config["physical_validation"] != "NOT_PERFORMED":
        print("FAIL: software must not self-certify physical validation", file=sys.stderr)
        return 2
    limit = float(config["temperature_limit_c"])
    scenarios = [
        ("dry_valid", dict(sensor_valid=True, ingress_detected=False, temperature_c=25, temperature_limit_c=limit), "NORMAL_MONITORING"),
        ("water_detected", dict(sensor_valid=True, ingress_detected=True, temperature_c=25, temperature_limit_c=limit), "CRITICAL_INGRESS_STOP"),
        ("sensor_missing_or_invalid", dict(sensor_valid=False, ingress_detected=False, temperature_c=25, temperature_limit_c=limit), "SENSOR_FAULT_SAFE_HOLD"),
        ("over_temperature", dict(sensor_valid=True, ingress_detected=False, temperature_c=limit, temperature_limit_c=limit), "THERMAL_WARNING"),
    ]
    checks = []
    for name, inputs, expected in scenarios:
        actual = classify(**inputs)
        checks.append({"scenario": name, "expected": expected, "actual": actual, "passed": actual == expected})
    passed = all(item["passed"] for item in checks)
    report = {
        "schema_version": "1.0",
        "project": config["project"],
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if passed else "FAIL",
        "checks_passed": sum(item["passed"] for item in checks),
        "checks_total": len(checks),
        "required_monitoring_signals": config["sensors"],
        "physical_validation": "NOT_PERFORMED",
        "waterproof_claim": "NOT_ESTABLISHED",
        "note": "Software contract simulation only; no physical sensor, enclosure, immersion or flood test was performed.",
        "scenarios": checks,
    }
    rendered = json.dumps(report, indent=2) + "\n"
    print(rendered, end="")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(
            f"## PUI89 water-resilience checks — {report['status']}\n\n"
            f"- Project: {config['project']}\n- Software scenarios: {report['checks_passed']}/{report['checks_total']} passed\n"
            "- Physical validation: NOT PERFORMED\n- Waterproof claim: NOT ESTABLISHED\n",
            encoding="utf-8",
        )
    return 0 if passed else 1

if __name__ == "__main__":
    raise SystemExit(main())

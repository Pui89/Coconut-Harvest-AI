"""Cross-check an experiment manifest against a held-out detector test report.

This audit checks provenance consistency; it does not certify dataset quality or model validity.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="JSON from create_experiment_manifest.py")
    parser.add_argument("--report", required=True, help="JSON from evaluate_detector.py")
    parser.add_argument("--output", default="reports/provenance_audit.json")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    report_path = Path(args.report).expanduser().resolve()
    manifest = read_json(manifest_path)
    report = read_json(report_path)
    checks: list[dict[str, Any]] = []

    def check(name: str, ok: bool, detail: str) -> None:
        checks.append({"check": name, "passed": bool(ok), "detail": detail})

    check(
        "test_evaluation_status",
        report.get("status") == "TEST_EVALUATION_FINISHED" and report.get("split") == "test",
        f"status={report.get('status')!r}, split={report.get('split')!r}",
    )
    dataset = manifest.get("dataset") if isinstance(manifest.get("dataset"), dict) else {}
    manifest_data_hash = dataset.get("yaml_sha256")
    report_data_hash = report.get("dataset_yaml_sha256")
    check(
        "dataset_yaml_checksum_matches",
        bool(manifest_data_hash) and bool(report_data_hash) and manifest_data_hash == report_data_hash,
        f"manifest={manifest_data_hash!r}; report={report_data_hash!r}",
    )
    manifest_weights = manifest.get("weights") if isinstance(manifest.get("weights"), dict) else None
    manifest_weights_hash = manifest_weights.get("sha256") if manifest_weights else None
    report_weights_hash = report.get("weights_sha256")
    check(
        "checkpoint_checksum_matches",
        bool(manifest_weights_hash) and bool(report_weights_hash) and manifest_weights_hash == report_weights_hash,
        f"manifest={manifest_weights_hash!r}; report={report_weights_hash!r}",
    )
    metrics = report.get("metrics")
    check(
        "metrics_present",
        isinstance(metrics, dict) and bool(metrics),
        "Metrics object is present" if isinstance(metrics, dict) and metrics else "No metric values found",
    )
    check(
        "manifest_not_claimed_as_result",
        manifest.get("status") == "MANIFEST_ONLY_NO_EXPERIMENT_RUN",
        f"manifest status={manifest.get('status')!r}",
    )

    passed = all(item["passed"] for item in checks)
    audit = {
        "schema_version": 1,
        "status": "PROVENANCE_CHECKS_PASSED" if passed else "PROVENANCE_CHECKS_FAILED",
        "audited_manifest": str(manifest_path),
        "audited_test_report": str(report_path),
        "checks": checks,
        "limitations": [
            "Passing checks show checksum consistency only; they do not prove the dataset is correctly labelled, legally reusable, independent, or representative.",
            "This script does not rerun training or evaluation and does not certify real-world or robot safety.",
            "Older evaluation reports without checksum fields must be regenerated using the updated evaluator.",
        ],
    }
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(audit, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"audit": str(output), "status": audit["status"], "checks": checks}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

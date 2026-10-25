"""Evaluate the deterministic project agent against synthetic, labelled scenarios.

This harness measures only local decision-workflow latency. It does not run an
ML model, inspect images, measure perception accuracy, access the network, or
control hardware. See docs/AGENT_EVALUATION_PROTOCOL.md.
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
import time
from pathlib import Path
from typing import Any

from agents.agentic_workflow import run_agentic_workflow

DEFAULT_INPUT = "examples/agentic_workflow.evaluation.json"
SIDE_EFFECT_FLAGS = (
    "execution_performed",
    "network_access_used",
    "model_inference_used",
    "actuator_commands_issued",
)


def _reject_constant(value: str) -> None:
    """Reject non-standard JSON constants such as NaN and Infinity."""
    raise ValueError(f"non-standard JSON constant is not allowed: {value}")


def load_scenarios(path: str | Path) -> dict[str, Any]:
    """Load and validate a synthetic evaluation manifest."""
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError("cannot read evaluation input file") from exc

    try:
        manifest = json.loads(raw, parse_constant=_reject_constant)
    except ValueError as exc:
        raise ValueError("evaluation file must contain valid finite JSON") from exc

    if not isinstance(manifest, dict):
        raise ValueError("evaluation root must be an object")
    if manifest.get("schema_version") != 1:
        raise ValueError("schema_version must be 1")
    if manifest.get("synthetic_only") is not True:
        raise ValueError("synthetic_only must be true")
    evaluation_id = manifest.get("evaluation_id")
    if not isinstance(evaluation_id, str) or not evaluation_id.strip():
        raise ValueError("evaluation_id must be a non-empty string")

    scenarios = manifest.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("scenarios must be a non-empty list")

    seen_ids: set[str] = set()
    for index, scenario in enumerate(scenarios):
        if not isinstance(scenario, dict):
            raise ValueError(f"scenario {index + 1} must be an object")
        scenario_id = scenario.get("scenario_id")
        if not isinstance(scenario_id, str) or not scenario_id.strip():
            raise ValueError(f"scenario {index + 1} needs a non-empty scenario_id")
        if scenario_id in seen_ids:
            raise ValueError("scenario_id values must be unique")
        seen_ids.add(scenario_id)
        if not isinstance(scenario.get("observation"), dict):
            raise ValueError(f"scenario {scenario_id} observation must be an object")
        expected = scenario.get("expected_decision_status")
        if not isinstance(expected, str) or not expected.strip():
            raise ValueError(f"scenario {scenario_id} needs an expected_decision_status")

    return manifest


def _check_invariants(report: Any) -> list[str]:
    """Return any failures in the review-only workflow contract."""
    failures: list[str] = []
    if not isinstance(report, dict):
        return ["workflow report is not an object"]

    if report.get("status") != "PROPOSAL_READY_FOR_HUMAN_REVIEW":
        failures.append("workflow did not return a reviewable proposal")
    if report.get("human_review_required") is not True:
        failures.append("human review is not explicitly required")
    for flag in SIDE_EFFECT_FLAGS:
        if report.get(flag) is not False:
            failures.append(f"{flag} must be false")

    digest = report.get("evidence_sha256")
    if (
        not isinstance(digest, str)
        or len(digest) != 64
        or any(character not in "0123456789abcdef" for character in digest)
    ):
        failures.append("evidence_sha256 is missing or malformed")

    decision = report.get("decision")
    if not isinstance(decision, dict):
        failures.append("decision is not a structured object")
    else:
        if decision.get("requires_human_approval") is not True:
            failures.append("decision does not require human approval")
        if decision.get("actuator_command") is not None:
            failures.append("decision contains a prohibited actuator command")
        if not isinstance(decision.get("status"), str):
            failures.append("decision status is missing")

    return failures


def evaluate_scenarios(manifest: dict[str, Any]) -> dict[str, Any]:
    """Run each scenario and report status matches, invariants and latency."""
    rows: list[dict[str, Any]] = []
    latencies: list[float] = []

    for scenario in manifest["scenarios"]:
        started = time.perf_counter_ns()
        try:
            workflow_report = run_agentic_workflow(scenario["observation"])
        except Exception:
            # Do not serialize exception text or observations into the report.
            workflow_report = None
        elapsed_ms = (time.perf_counter_ns() - started) / 1_000_000
        latencies.append(elapsed_ms)

        failures = _check_invariants(workflow_report)
        decision = (
            workflow_report.get("decision")
            if isinstance(workflow_report, dict)
            else None
        )
        observed_status = decision.get("status") if isinstance(decision, dict) else None
        expected_status = scenario["expected_decision_status"]
        if observed_status != expected_status:
            failures.append("decision status did not match the expected status")

        rows.append(
            {
                "scenario_id": scenario["scenario_id"],
                "expected_decision_status": expected_status,
                "observed_decision_status": observed_status,
                "workflow_status": (
                    workflow_report.get("status")
                    if isinstance(workflow_report, dict)
                    else "WORKFLOW_ERROR"
                ),
                "project": (
                    workflow_report.get("project")
                    if isinstance(workflow_report, dict)
                    else None
                ),
                "evidence_sha256": (
                    workflow_report.get("evidence_sha256")
                    if isinstance(workflow_report, dict)
                    else None
                ),
                "latency_ms": round(elapsed_ms, 3),
                "passed": not failures,
                "failures": failures,
            }
        )

    total = len(rows)
    passed = sum(1 for row in rows if row["passed"])
    sorted_latencies = sorted(latencies)
    p95_index = max(0, math.ceil(0.95 * len(sorted_latencies)) - 1)
    metrics = {
        "scenario_count": total,
        "passed_count": passed,
        "failed_count": total - passed,
        "pass_rate": round(passed / total, 4) if total else 0.0,
        "mean_latency_ms": round(statistics.fmean(latencies), 3) if latencies else None,
        "p95_latency_ms": round(sorted_latencies[p95_index], 3) if sorted_latencies else None,
        "max_latency_ms": round(max(latencies), 3) if latencies else None,
    }

    return {
        "schema_version": 1,
        "evaluation_id": manifest["evaluation_id"],
        "synthetic_only": True,
        "result": "PASS" if passed == total else "FAIL",
        "project": rows[0].get("project"),
        "metrics": metrics,
        "resource_profile": {
            "third_party_packages_required": False,
            "network_access_used": False,
            "model_inference_used": False,
            "hardware_actuation_used": False,
            "peak_memory_measured": False,
            "latency_scope": "local deterministic decision workflow only",
        },
        "scenarios": rows,
        "limitations": [
            "Synthetic scenarios test decision logic, not real-world perception or decision quality.",
            "Latency excludes image capture, sensors, model inference, communications and hardware.",
            "Peak memory, CPU utilisation, GPU utilisation and energy were not measured.",
            "A passing result does not validate a physical robot or authorize operational use.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run a no-dependency synthetic evaluation of the existing local decision workflow."
    )
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT,
        metavar="PATH",
        help="synthetic evaluation JSON file",
    )
    parser.add_argument(
        "--output",
        default="-",
        metavar="PATH",
        help="report path or '-' for stdout",
    )
    args = parser.parse_args(argv)

    try:
        manifest = load_scenarios(args.input)
        report = evaluate_scenarios(manifest)
    except ValueError as exc:
        print(f"evaluation input error: {exc}", file=sys.stderr)
        return 2

    rendered = json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.output == "-":
        sys.stdout.write(rendered)
    else:
        try:
            Path(args.output).write_text(rendered, encoding="utf-8")
        except OSError:
            print("evaluation output error: cannot write report file", file=sys.stderr)
            return 2
        print(
            f"Evaluation result: {report['result']} "
            f"({report['metrics']['passed_count']}/{report['metrics']['scenario_count']} scenarios)"
        )
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

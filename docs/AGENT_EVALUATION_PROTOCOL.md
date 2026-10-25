# Synthetic Agent Evaluation Protocol

## Purpose

This no-dependency harness checks whether the existing deterministic decision agent produces expected statuses for named synthetic cases and preserves non-negotiable safety invariants. It records repeatable evidence hashes and local workflow latency.

## Run locally

From the repository root:

```bash
python -m unittest discover -s tests -p "test_evaluate_agentic_workflow.py"
python -m tools.evaluate_agentic_workflow
```

To save a report:

```bash
python -m tools.evaluate_agentic_workflow --input examples/agentic_workflow.evaluation.json --output agent-evaluation-report.json
```

The report contains case IDs, expected/observed decision status, input hash, pass/fail and timings. The observations themselves are deliberately not copied into the report.

## What is measured

- Status match between the decision agent and each labelled synthetic scenario.
- Explicit human-review and human-approval requirements.
- Explicitly false flags for network access, model inference, hardware actuation and workflow execution.
- Canonical input SHA-256 as a reproducibility identifier.
- Wall-clock latency of the local deterministic decision workflow.

## What is not measured

This is **not** a perception benchmark, model benchmark, robot test or deployment safety case. It does not evaluate real images, dataset accuracy, physical motion, sensor quality, rescue performance, chemical identification, or the quality of human decisions. Latency excludes image capture, sensors, model inference, network communication and hardware. Peak RAM, CPU/GPU utilisation and energy consumption are intentionally not claimed as measured.

A PASS means only that the checked synthetic cases matched their expected decision statuses and safety invariants. Any real-world use still needs representative, licensed data; independently reviewed ground truth; domain-specific validation; human oversight; and platform-specific physical testing where applicable.

## Project-specific boundaries

- **Coconut Harvest AI:** status checks do not establish coconut detection accuracy, maturity classification accuracy, 0–30 m reach, or a validated harvesting robot.
- **Multimodal Narcotics Screening AI:** status checks do not identify a substance, establish contraband, infer guilt, or authorize enforcement. Expert human review is required for any real screening workflow.
- **Extreme Flood Rescue AI:** simulated status checks do not prove flood navigation, buoyancy, waterproofing, victim detection, rescue capability or operation at any particular water depth.

## Adversarial workflow regression

The separate `tests/test_agentic_workflow_stress.py` suite mutates synthetic observations with invalid types, misleading approval values, conflicting safety flags, nested untrusted command-like fields, non-finite numbers, and injected project-agent failures. It asserts review-required output and false network/model/execution/actuator flags. This is a bounded regression matrix, not formal verification or a complete security audit.

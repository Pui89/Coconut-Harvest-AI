# Embodied Agent Evaluation Core

This repository includes a small, standard-library evaluation helper intended to make test records consistent across Pui89 projects.

## What it does

- Validates a common case-result schema.
- Counts pass, fail and blocked cases.
- Reports pass rate only for completed pass/fail cases; blocked cases are excluded.
- Rejects a pass record that contains listed safety violations.
- Flags duplicate case IDs and malformed records.
- Writes a JSON report with a UTC timestamp and an explicit limitation note.

## What it does not do

- It does not execute an agent, simulate physics, or control hardware.
- It does not determine whether a task evaluator is correct.
- It does not turn synthetic or simulated results into real-world evidence.
- It does not prove safety, reliability, or field readiness.

## Result schema

Each result is a JSON-compatible object with:

- `case_id`: unique identifier within the report.
- `scenario`: short scenario name.
- `expected`: evaluator-defined expected outcome.
- `observed`: evaluator-recorded outcome.
- `status`: `pass`, `fail`, or `blocked`.
- `safety_violations`: optional list of identified safety violations.

Optional fields can record project-specific evidence, such as image IDs, water depth, modality, latency, or reviewer notes. Keep source provenance and license evidence with dataset records, not just in this summary.

## Example

```python
from tools.embodied_eval import write_report

results = [
    {
        "case_id": "scenario-001",
        "scenario": "replace-with-a-real-test-scenario",
        "expected": "expected outcome",
        "observed": "observed outcome",
        "status": "blocked",
        "safety_violations": [],
        "notes": "No evaluator evidence recorded yet.",
    }
]
write_report("replace-with-project-name", results, "reports/evaluation.json")
```

Run the focused tests with:

```bash
python -m pytest tests/test_embodied_eval.py
```

No new runtime dependency, model download, cloud service, or robot actuation is required. The example above is illustrative only; it is not a project test result.

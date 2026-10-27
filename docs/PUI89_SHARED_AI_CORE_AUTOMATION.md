# PUI89 Shared AI-Core Automation Contract

Status: initial smoke-test contract; not a validated robot controller.

This contract is mirrored across the three PUI89 AI application repositories to reduce integration drift. It standardizes the minimum checks that should run before project-specific model or simulation tests.

## Required interface concepts

- **Observation:** source, value, confidence in the inclusive range 0–1, and timestamp.
- **World state:** named observations plus explicit uncertainty flags.
- **Action proposal:** proposed action, confidence, simulation-only status, and whether human review is required.
- **Safety gate:** fail closed for unknown state, invalid/low confidence, missing required human approval, or any physical action in this smoke-test layer.
- **Failure report:** stable case ID, expected result, actual result, severity, and pass/fail status.
- **Reproducibility:** save machine-readable JSON output with test count, failures, runtime, UTC timestamp, and a scope note.

## Project-specific extensions

- Coconut Harvest: maturity label, target localization, harvestability, tree/obstacle state, and dataset provenance.
- Extreme Flood Rescue: person/animal candidate, visibility and water-state estimates, navigation confidence, and simulated route outcome.
- Multimodal Screening: modality availability, fused confidence, calibration status, abstention reason, and human-review decision.

## Execution order

1. Run standard-library contract smoke tests.
2. Run existing repository unit tests and static/data validators.
3. Run deterministic simulation scenarios and preserve failure reports.
4. Record model metrics only when computed from a documented, versioned evaluation set.
5. Evaluate optional local VLM/VLA components only after checking licence, disk, RAM and VRAM requirements.

No model accuracy, field performance, chemical detection, flood-depth capability, or physical robot capability is implied by passing these interface tests.

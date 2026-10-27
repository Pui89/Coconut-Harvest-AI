# PUI89 Shared AI Core Contract (v1)

## Purpose

This small, standard-library-only contract is copied into the three PUI89 projects so their perception and planning code can use the same vocabulary for observations, uncertainty, stale data, unknown state, and conflicts.

## Interface

- `Observation`: value, source provenance, observation timestamp, confidence in [0, 1], and optional calibration status.
- `assess_observation(...)`: returns `ACCEPT`, `REVIEW`, or `REJECT` with machine-readable reason codes.
- `WorldState`: timestamped observation ledger with conservative conflict checks.
- `may_actuate_hardware`: always false by design. Acceptance only means eligible for downstream planning or simulation; it is not permission to operate a physical robot.

## Decision policy

- Missing values and invalid confidence or future timestamps are rejected.
- Stale, low-confidence, missing-provenance, missing-timestamp, uncalibrated, or explicitly review-required observations go to review.
- Unknown world state is rejected.
- Conflicting fresh observations go to review.
- No model, dataset, simulator, or physical robot is considered validated by these software tests.

## Run tests

From the repository root, using Python 3.10+:

```bash
python -m unittest discover -s tests -p "test_pui89_world_state.py" -v
```

The tests use only the Python standard library. They do not install packages, download models, contact a hosted API, or control hardware.

## Project-specific use

- **Coconut Harvest AI:** use confidence and freshness gates before target-localization or harvestability proposals; actual reachability and cutting safety remain separate validation tasks.
- **Extreme Flood Rescue AI:** treat stale/conflicting water, current, localization, and person/animal observations conservatively; this contract is not flood physics or rescue validation.
- **Multimodal Narcotics Screening AI:** missing or uncertain modalities should trigger review, never an automatic chemical-identification claim; human review and lawful dataset validation remain necessary.

## Status

This file and its tests are an engineering scaffold. Run the command and record the actual output before describing the tests as passed. No accuracy, latency, calibration quality, or field performance is claimed.

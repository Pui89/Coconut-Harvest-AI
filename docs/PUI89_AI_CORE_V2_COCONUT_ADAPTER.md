# PUI89 AI Core v2 — Coconut Harvest AI Adapter

**Status:** First-project reference integration; software-only baseline.

The initial standard-library gate implementation is in `pui89_core_v2/`. It is deliberately advisory: it evaluates a proposal and returns a structured gate decision. It does not control a robot, motor, cutter, gripper, or other hardware.

## Current behavior

- Checks proposal and World State linkage.
- Requires a current, timezone-aware World State timestamp.
- Holds on unknown, conflicted, stale, or evidence-free claims.
- Requires supporting observations to exist, be valid, and have verified source integrity.
- Holds on critical, high, or unknown risk.
- Requires explicit human authorization both in the proposal and at the gate call.
- Returns `ALLOW_FOR_HUMAN_REVIEW` only when baseline checks pass; this is not an execution permit.

## Run the tests

From the repository root, in an existing Python environment with pytest available:

```bash
python -m pytest tests/test_pui89_core_v2_safety.py
```

No model downloads, cloud services, new runtime packages, or hardware are required.

## Next integration work

1. Map current Coconut observations into the shared Observation contract.
2. Replace any project-specific duplicate gate only after parity tests demonstrate equivalent or stronger safety behavior.
3. Add domain interlocks for worker/animal exclusion, arm workspace, reach, cutter state, and emergency stop.
4. Keep all physical actuation disabled until hardware-specific interlocks and independent validation exist.

This adapter is a first reference implementation, not evidence of a trained detector, safe harvesting, or physical robot readiness.

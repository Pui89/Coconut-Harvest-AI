# Autonomous system supervisor — Coconut Harvest AI

## Purpose

This project includes a small, dependency-free **software decision gate** for an autonomous-system workflow. It converts explicitly supplied health, authorization, hazard, and confidence values into one of four advisory modes:

- `autonomous_candidate`: supplied software checks pass; this is not permission to bypass application or hardware safety controls.
- `safe_hold`: required sensing, localization, communication, hazard clearance, or confidence is not confirmed.
- `manual_recovery`: authorization or task validity is missing.
- `stopped`: emergency stop is active or the safety monitor is unhealthy.

## Project-specific inputs to validate

For Coconut Harvest AI, relevant inputs include: coconut detector output, maturity estimate, depth/range, localization, obstacle clearance.

Hazards that must be represented in application-level checks include: uncertain target or maturity, unknown tree height/reach, people in exclusion zone, camera/depth failure, unstable platform.

These values must come from trusted application logic or sensors and must be checked for freshness, calibration, validity, and provenance. The current module accepts values; it does **not** acquire sensors, detect hazards, estimate location, or verify the truth of a model prediction.

## Run the unit tests

From the repository root, using Python 3.10 or newer:

```bat
python -m unittest discover -s tests -p "test_autonomy_supervisor.py" -v
```

This test command uses Python's standard library and requires no extra package. It has not been run on your computer; check the CI or execute it locally before treating it as verified.

## Safety boundary

- No motor, cutter, steering, boat, drone, conveyor, or other actuator command is implemented here.
- A `stopped` software decision does not physically stop hardware. A separate, independently validated safety circuit and emergency-stop path are required for physical systems.
- The system must not infer that a hazard is absent merely because a sensor or model returned no detection.
- Human authorization and domain-specific rules remain required for consequential actions.
- For screening, model output is triage evidence only—not proof of a substance's identity or a person's guilt.
- For rescue and harvesting, unknown environmental conditions or reachability must block hazardous action.

## Integration sequence

1. Connect only existing, validated software status signals to `SystemStatus`.
2. Log the input values, timestamp, data source, decision mode, and reasons; avoid logging sensitive personal data unnecessarily.
3. Test missing, stale, contradictory, non-finite, and out-of-range values.
4. Exercise simulated failures and confirm the application transitions to hold/recovery.
5. Review false-safe cases independently before any field trial.
6. Keep physical actuation disabled until a separate hardware safety design is implemented and validated.

## Evidence status

This is a rule-based autonomy-supervision component with unit tests. It is not an autonomous robot, a trained perception model, or evidence of field-ready operation. Passing unit tests would verify these software rules only.

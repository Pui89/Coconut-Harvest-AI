# Automated verification and evidence report

**Status:** regression-test harness for software policy and scenario configuration. It is not evidence of robot accuracy, physical safety, or field readiness.

## What this adds

- A standard-library-only regression suite for the shared PUI89 autonomy lab.
- Negative tests for emergency stop, sensor faults, stale data, communication loss, malformed safety flags, low/invalid confidence, conflicting or missing modalities, missing targets, and high-impact screening actions.
- Scenario-config checks for duplicate IDs, invalid confidence thresholds, and non-positive step durations.
- Stable JSON/digest checks that support reproducible scenario configuration fingerprints.

## Run locally or in an existing test environment

```bash
python -m unittest discover -s tests -p "test_*.py"
```

The test suite does not install packages, download models, call external services, access hardware, or actuate a robot. It is intentionally not wired to a new scheduled workflow, avoiding unnecessary recurring compute.

## Project-specific evidence boundaries

- **Coconut Harvest AI:** policy tests do not measure maturity classification accuracy, fruit localization, cutting precision, reach, or dropped-fruit risk.
- **Extreme Flood Rescue AI:** policy tests do not validate flood depth/current handling, localization, braking, buoyancy, or real rescue capability. The 15 m target remains simulation-only unless separately validated.
- **Multimodal Narcotics Screening AI:** policy tests do not validate chemical sensing or substance identification. Alerts are triage signals only; ambiguous or conflicting evidence must remain unknown or require qualified human review.

## Interpreting results

A passing test means only that the tested software behavior matched its assertion in that run. It does not mean an untested feature passed. Keep **PASS**, **FAIL**, and **NOT TESTED** distinct. Record Python version, commit SHA, test command, scenario/data version, and test output when publishing evidence. Do not publish accuracy claims without appropriately sourced, held-out, representative test data.

Before any physical deployment, perform project-specific risk assessment, independent hardware safety design, instrumented testing, and qualified review. Never use these software tests as a substitute for worker or animal exclusion, emergency-stop hardware, or other protective measures.

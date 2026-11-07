# Coconut Harvest AI — Shared AI Core adoption

**Implementation status:** project-side Python adapters and contract tests are proposed in PR review.  
**Contract version:** `0.1.0-draft`  
**Pinned schema source:** [PUI89 Shared AI Core schemas at commit `2d9eeb465e6ab571e7391ef6b78b72d4007ba7e5`](https://github.com/Pui89/Pui89.github.io/tree/2d9eeb465e6ab571e7391ef6b78b72d4007ba7e5/schemas/pui89)

## What this change integrates

- `pui89_core/contracts.py` provides standard-library Python records for Observation, WorldState, ActionProposal and FailureReport.
- `tools/pui89_coconut_contract_adapter.py` maps an explicitly supplied, already-validated VisionFinding into an Observation.
- Tests cover provenance, timestamps, modality, confidence bounds, missing evidence, unique evidence references, uncertainty, human approval and prohibited actuation.
- The existing project-specific autonomy, tracking and reporting code remains in place; this is an adapter layer, not a destructive rewrite.

## Safety and evidence boundaries

- The schema source is pinned to a commit, not fetched at runtime. No network request or package installation is needed by the adapter.
- The pinned central schemas are still marked `0.1.0-draft`. The project adapter is a draft-compatible implementation, not a released package and not proof of integration across all projects.
- The adapter accepts caller-supplied findings only. It does not run a detector or independently establish coconut maturity.
- Confidence is retained as an input score and explicitly marked uncalibrated/unknown. It must not be interpreted as calibrated probability.
- Dataset rights default to `unknown`; integrity defaults to `unverified`. The adapter never promotes either status automatically.
- Action proposals require human approval, are advisory-only, remain simulation-only, and cannot actuate hardware.
- These software checks do not validate the 0–30 m operating target, detector accuracy, cutting, reach, stability or physical safety.

## Verification

Run the existing lightweight core workflow, or locally run:

```bash
python -m unittest discover -s tests -p "test_pui89_shared_contracts.py" -v
```

No new runtime dependency, model download, paid API, cloud GPU or hardware command is introduced.

## Adoption gate

After this PR's tests pass, review the schema revision and mapping. Then migrate the next PUI89 project using the same pinned contract source and project-specific adapter tests. Do not change the central draft version silently; any schema change must update the pinned source and compatibility tests.

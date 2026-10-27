# Shared PUI89 AI Core — Coconut Harvest adapter

**Status:** integration contract and test plan. This is not a claim that a trained detector or physical harvesting robot has been validated.

## Shared contract

Use the repository's existing standard-library autonomy lab and world-state/report modules as the Phase 1 foundation. Project adapters should expose normalized observations, a conservative decision, and structured evidence; they must not import a model or simulator as a side effect.

A scenario record should include scenario_id, seed_label, timestamp, source_group, observations, expected_mode, and expected_action. Each observation should preserve source/hash where applicable, timestamp/freshness, quality/confidence, and an explicit missing/unknown state. Each result should record actual mode/action, guard trace, failure codes, elapsed time, code revision, configuration hash, and limitations.

## Coconut-specific test matrix

- Candidate image has no verified source or reuse terms → keep it out of training; emit a provenance failure.
- File hash differs from the source record → reject the record for review; never silently update the expected hash.
- Box coordinates are malformed, out of bounds, or use the wrong convention → fail annotation QA.
- Human review is absent or unresolved → do not promote a draft label to approved.
- Same tree/source/session appears across train and test → fail split-leakage audit.
- Maturity class, fruit identity, height metadata, or reach estimate is unknown/conflicting → return UNKNOWN / REQUEST_REVIEW; do not propose a cut.
- Any reach, stability, collision clearance, tool readiness, or approval gate fails → SAFE_HOLD; no actuator interface is permitted.

## Height and metrics

The 0–30 m range and four maturity categories remain design targets until supported by measured, licensed, reviewed examples and separate physical evidence. Record height_m=null and height_status=unverified when height is not measured. Split by tree/orchard/source/session, not adjacent frames. Report precision, recall, F1/mAP and latency only when measured on an eligible held-out set, with class counts and uncertainty.

## Run order

1. Run python tools/pui89_master_verify.py.
2. Run the existing standard-library autonomy-lab tests and scenario runner documented in docs/PUI89_AUTONOMY_LAB.md.
3. Run provenance/hash and annotation QA on local candidate files; do not download or approve data automatically.
4. Publish the exact command, commit, report, failures, and NOT RUN items.

**Cost and safety:** no paid API, cloud GPU, model download, package installation, or hardware action is part of this contract.
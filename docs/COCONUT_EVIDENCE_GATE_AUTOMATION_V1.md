# Coconut Harvest AI — Evidence Gate Automation v1

**Status:** proposed automation; draft PR only until reviewed and merged.

## Purpose

Run the existing standard-library dataset preflight automatically so the project can see whether recorded source-rights metadata, candidate-review records, and annotation geometry have changed. The workflow is a monitor, not an approval authority.

## Triggers

- Daily at 05:45 Asia/Bangkok (22:45 UTC).
- On pull requests and pushes to `main` when the rights/review ledgers, candidate-0032 draft, preflight tools, or execution-gate document change.
- Manual GitHub Actions dispatch.

## Checks

The workflow reuses `tools/run_coconut_dataset_preflight.py` and its existing components:

1. Parse and geometry-check the candidate-0032 draft annotations.
2. Reconcile the source-rights and candidate-review CSV ledgers.
3. Count eligible and blocked candidates and report the top recorded blockers.
4. Report candidate-0032 source-byte verification as `NOT_CHECKED` unless the exact local original image is explicitly supplied to a local run.

## Expected current result

The current dataset is expected to remain blocked/incomplete: the dated readiness snapshot records 34 candidates and 0 eligible for training. The workflow treats the preflight's expected blocked exit code as a reportable status, not as a broken CI job. An execution error still fails the job.

## Strict safety boundaries

- The workflow is read-only and uses `contents: read`.
- It does not download or upload source images.
- It does not modify CSV ledgers, annotations, hashes, labels, human-QA flags, or training approvals.
- It does not train a model, calculate detector accuracy, or authorize physical robot operations.
- It cannot independently establish licence validity or confirm that human visual review actually occurred.
- Candidate 0032's source hash must be checked against the exact original local bytes using the documented local helper. The hosted workflow must not guess, fetch, or substitute an image.

## Acceptance criteria

- Workflow completes on current repository data and reports the blocked state accurately.
- Geometry, promotion-gate, and source-fingerprint statuses remain separate.
- A successful CI run is never described as dataset approval.
- Existing project workflows remain unchanged.

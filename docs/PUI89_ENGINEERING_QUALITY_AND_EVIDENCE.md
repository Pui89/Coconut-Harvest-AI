# PUI89 Engineering Quality and Evidence System — Coconut Harvest AI

**Reviewed:** 25 October 2026  
**Purpose:** a lightweight, free-first release gate shared across PUI89 projects. This is a process standard, not a claim that the project is validated.

## Non-negotiable evidence rules

1. **No evidence, no claim.** Use *verified*, *failed*, *not measured*, or *blocked* with a named artifact, test, dataset/scenario, and date.
2. **Separate software, simulation, model, and physical evidence.** A passing unit test or CI job does not establish detector accuracy or safe physical harvesting.
3. **Reproducibility before performance claims.** Record code revision, environment, command, data/source provenance, split protocol, sample count, metrics, failures, and report path.
4. **No fabricated numbers.** Do not fill gaps with estimates or synthetic fixture values. Label synthetic results explicitly.
5. **Free-first.** Prefer local tools and Python standard library where suitable. Do not require paid APIs, hosted GPUs, subscriptions, or model downloads for basic checks. Warn before any resource-heavy download.
6. **Safe, reversible workflow.** Work on a branch and open a reviewable pull request. Do not auto-merge or silently modify the default branch.
7. **Human review for consequential decisions.** AI output remains advisory until independently validated and appropriately reviewed.

## Project release gates

| Gate | Required evidence | Current status |
|---|---|---|
| Source and dataset rights | Source URL, creator, license/permission, retrieval date, checksum where available | **In progress**; audit each candidate |
| Annotation quality | Native-resolution labels, coordinate/geometry validation, independent visual review, documented exclusions | **Blocked** until required reviews are complete |
| Dataset split integrity | Group/tree/source/session-aware split; duplicate/leakage checks and split version | **Not yet demonstrated for a training-ready dataset** |
| Detector baseline | Frozen labelled holdout; precision, recall, F1/mAP as appropriate; sample count, failures, latency and environment | **Not measured on an approved training-ready dataset** |
| Harvest workflow | Explicit tests for target uncertainty, occlusion, reachability, collision gate, safe hold and operator approval | Software tests only; no physical harvest validation |
| Physical capability | Instrumented orchard trials, safety review, repeat trials, documented operating envelope | **Not validated** |

## Standard evidence record

For each meaningful test or experiment, record:

- **ID / requirement:** stable identifier and expected behavior.
- **Revision and environment:** commit SHA, OS, Python/dependency versions, hardware if relevant.
- **Command and inputs:** exact command, dataset/scenario version, source/license and split details.
- **Result:** pass/fail/blocked/not measured; actual counts and metrics only when observed.
- **Failures and uncertainty:** false positives/negatives, exceptions, abstentions and excluded cases.
- **Artifact:** durable report path or CI run URL.
- **Limitations and next action:** what the result does not establish.

## Operating loop

1. Select one measurable requirement from [the validation matrix](VALIDATION_MATRIX.md) and [research evidence checklist](RESEARCH_EVIDENCE_CHECKLIST.md).
2. Make the smallest safe change on a dedicated branch.
3. Run the narrow relevant tests first; then the repository regression suite when feasible.
4. Inspect logs and generated artifacts. A command completing is not sufficient if assertions or report checks fail.
5. Update the validation matrix with observed evidence and limitations.
6. Open a pull request with scope, commands run, results, and unrun checks; review before merging.

## Immediate priority

Unblock the coconut dataset before model claims: resolve candidate source/rights records, native-resolution annotation geometry, independent visual QA, and group-aware splits. Candidate 0034 is not training eligible while it has no box coordinates and visual review remains outstanding. Do not train on it or invent a benchmark result.

## Completion criteria

This system is operational only when a reviewer can trace **requirement → implementation → test → observed result → artifact → limitation**. The document itself does not certify the system, dataset, detector, or robot.

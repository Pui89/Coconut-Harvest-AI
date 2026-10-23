# Engineering Requirements and Evidence Matrix

**Purpose:** Track what is implemented, what has been tested, and what still needs real evidence. This is an engineering checklist, not a certification or claim of field readiness.

**Evidence rule:** A passing software test verifies only the tested software behavior. It does not establish detector accuracy, legal image rights, physical safety, or successful harvesting. Do not promote dataset candidates or claim performance without the required independent evidence.

## Status definitions

- **Verified:** the named check ran and its result is linked or recorded.
- **Failed:** a check ran and did not meet its stated criterion.
- **Not measured:** evidence is not yet available; do not infer a pass.
- **Blocked:** a prerequisite is missing, so the downstream test must not be treated as valid.

## Requirements and evidence

| ID | Requirement / metric | Test method | Dataset / scenario | Baseline or pass criterion | Current evidence status | Next action |
|---|---|---|---|---|---|---|
| DATA-01 | Every candidate has traceable source, creator, licence, and attribution | Review source page and rights ledger entry individually | Candidate image; source URL recorded in rights ledger | Each source is independently reviewed; recorded fields alone are insufficient | **Blocked** — 34 candidate records are recorded; 0 approved for training in the latest documented snapshot | Review rights and attribution per candidate; record evidence and reviewer |
| DATA-02 | Labels represent visible, distinguishable coconuts | Inspect original-resolution image and annotation overlay | Human-reviewed real images | Independent visual QA passes; hidden or ambiguous fruit are not guessed | **Not measured** for full dataset | Annotate suitable images; review overlays independently; keep unverified candidates blocked |
| DATA-03 | Training and evaluation data are separated without source leakage | Run duplicate and source/tree/session split audits | Rights-cleared, human-reviewed images | No known duplicate or same-source leakage across train/validation/test | **Blocked** until enough approved data and source metadata exist | Record source/session grouping, audit duplicates, freeze split manifest |
| DATA-04 | Dataset promotion gate rejects incomplete evidence | Run promotion-gate CLI and its unit tests | Rights and review CSV ledgers | Missing rights/QA/approval fields must block promotion; malformed inputs must not silently pass | CI test coverage added; real dataset remains blocked | Check latest CI and inspect generated readiness JSON artifact |
| AI-01 | Coconut detection and maturity classification have measured performance | Evaluate predictions against human-reviewed ground truth; report per-class precision, recall, F1 and IoU as appropriate | Frozen, held-out real-coconut test set | Report sample counts and exact protocol; no invented threshold or score | **Not measured** — no approved held-out set documented | Build the held-out set only after rights and annotation gates pass |
| AI-02 | Performance is examined across lighting, occlusion, distance, and maturity | Stratified evaluation where each subgroup has adequate labels | Held-out real images with condition labels | Report each available subgroup and its sample count; identify unsupported groups | **Not measured** | Add condition labels during review where visible and defensible |
| ROBOT-01 | Cutting is inhibited when perception, localization, reachability, or sensor state is uncertain | Unit and fault-injection tests against decision logic | Synthetic inputs and software fixtures | Unsafe, missing, malformed, NaN/Inf, or contradictory inputs lead to a conservative no-cut result | Software checks only; physical interlocks are unverified | Expand negative tests; separately specify independent hardware interlocks |
| ROBOT-02 | The proposed 0–30 m tree-height envelope is not presented as demonstrated capability | Review documentation and concept assumptions | Design concept; simulation only unless physical measurements are added | Label as an aspiration/design envelope until measured; state reach and stability limits as unknown | Concept only; physical reach not validated | Define staged simulation cases; do not invent reach, payload, wind, or stability values |
| DEMO-01 | A small, repeatable local software demonstration can be run without paid APIs | Follow documented commands in a clean environment | Synthetic or sample inputs clearly labelled | Command, versions, expected output, and actual result are recorded | **Not measured here** | Run the documented quickstart locally or in free CI; report environment and result |
| PERF-01 | Runtime and resource use are reproducible | Record command, versions, device, latency, memory and sample count | Same frozen evaluation input and environment | Report measured values and limitations; no extrapolation to robot operation | **Not measured** for real-coconut evaluation | Measure only after a valid evaluation set and runnable model exist |
| DOC-01 | Public claims match code and evidence | Review README, workflow, reports, and links together | Repository at a specific commit | Clearly distinguish implemented, tested, evaluated, conceptual, and planned | Partial: README documents limitations; dated status snapshot can become stale | Refresh status only after checking the latest commit and completed CI runs |

## Release / maturity gate

Use the least advanced label supported by evidence:

1. **Software prototype:** code exists; tests may cover selected behavior.
2. **Tested software prototype:** named regression tests pass on a recorded commit.
3. **Evaluated AI prototype:** a lawful, labelled, held-out dataset and reproducible metrics exist.
4. **Simulation-evaluated system:** repeatable end-to-end simulation results exist and are clearly separated from physical results.
5. **Physical prototype evaluated:** documented staged physical tests and measured outcomes exist.

Passing CI alone never advances the project to an AI-accuracy or physical-robot claim.

## Reproducibility record template

For each future evaluation, record:

- Commit SHA and date
- Exact command and dependency/runtime versions
- Hardware / operating system
- Dataset version, source groups, split, and sample count
- Baseline and metric definitions
- Actual output, test result, and artifact URL
- Failures, uncertainty, limitations, and next action

## Immediate priority

Keep the coconut dataset blocked for training until rights, annotation correctness, independent QA, and leakage-safe splits have been verified. Do not change any candidate to approved merely because a structural checker passes.

# Engineering Assurance and Verification Plan

**Status:** engineering process document for a research prototype.  
**Basis:** practices adapted from public NASA systems-engineering and software-assurance guidance. This is not NASA approval, certification, or a claim of compliance with NASA standards.

## 1. Purpose and system boundary

This plan makes requirements, hazards, tests, and evidence traceable for the Coconut Harvest AI software and proposed agricultural robot.

**Implemented software scope:** rule-based planning, synthetic workflow demo, manual image-review and annotation-QA utilities.  
**Not established:** reliable real-orchard detection or maturity classification, calibrated 3D localization, physical cutting, fruit retention/lowering, or autonomous operation across palm heights of 0–30 m.

Software output must never directly authorize a physical cut. Any future actuator integration requires separate safety engineering, hardware interlocks, risk assessment, and qualified review.

## 2. Requirements and verification matrix

| ID | Requirement | Verification | Acceptance evidence | Current status |
|---|---|---|---|---|
| CH-REQ-001 | Invalid or missing candidate inputs are rejected or marked invalid. | Unit/regression tests | Tests for missing fields, wrong types, non-finite values, boundaries. | Must be confirmed by CI. |
| CH-REQ-002 | A software recommendation cannot authorize physical cutting. | Code inspection and workflow tests | No actuator command path in current prototype; future integration requires explicit approval and independent interlocks. | Stated boundary; re-check on integration. |
| CH-REQ-003 | Uncertain, occluded, unlocalized, or out-of-range fruit cannot be treated as harvest-ready. | Scenario tests | Review, survey-only, or no-cut outcome. | Intended policy; verify each path. |
| CH-REQ-004 | Real-image metrics identify data provenance, labels, split, metric definitions, and failures. | Benchmark/report audit | Reproducible held-out results and explicit limitations. | Reliable trained-detector benchmark not established. |
| CH-REQ-005 | Dataset rights and annotation quality are checked before training or redistribution. | Source/manifest audit | Source, licence or permission, retrieval date, and review status recorded. | In progress. |
| CH-REQ-006 | Harvest success requires confirmed outcome, not detection or planning alone. | Acceptance review | Confirmed, failed, and unknown outcomes separated. | Physical harvesting not demonstrated. |

## 3. Initial hazard log

| Hazard | Potential consequence | Required control before physical trials |
|---|---|---|
| Incorrect maturity classification | Wrong fruit selected or crop damage | Validated class criteria, independent test set, human confirmation |
| Incorrect 3D position or reach estimate | Collision, dropped tool, injury | Calibrated sensors, verified workspace and conservative reach envelope |
| Unexpected cutter activation | Severe injury or damage | Guarded tool, independent hardware interlock, emergency stop; no AI-only activation |
| Fruit falls or is not retained | Injury or property damage | Engineered retention/lowering, exclusion zone, outcome verification |
| Power, communication, or sensor loss | Unsafe or stale action | Fail-safe stop; invalid/stale input cannot preserve an actionable plan |
| Misleading benchmark or concept image | Capability overstatement | Label synthetic, conceptual, and unvalidated evidence |

This is an initial hazard log, not a completed formal safety analysis. Add owners, severity/likelihood ratings, mitigations, and closure evidence before hardware trials.

## 4. Verification, validation, and release gates

1. **Software:** tests pass on supported Python versions; invalid-input and fail-closed cases are covered.
2. **Data:** rights, annotation rules, independent group-aware splits, and dataset version are recorded.
3. **Model:** evaluate a baseline on held-out real orchard images; report per-class precision/recall, false positives/negatives, latency, uncertainty, and failures. Do not hide failed baselines.
4. **Simulation:** repeatable seeded scenarios cover occlusion, mixed maturity, reach limits, sensor loss, and stop behaviour.
5. **Hardware:** no actuator trial until qualified reviewers approve risk assessment, guarding, emergency stop, independent interlocks, and supervised procedure.
6. **Field:** no reliable-harvesting or 0–30 m capability claim without documented representative field tests and independent review.

Verification checks whether requirements are met; validation checks whether the system suits its intended use. Passing software tests is not proof of field performance.

## 5. Evidence and change control

For each result, record commit, environment, command, dataset/model version, seed where relevant, raw output, metric definitions, and limitations. Keep datasets and weights out of Git unless rights and policy allow them. Safety-related changes require updated tests and human review.

## 6. Cost and licensing

Prefer local execution and free/open-source tools. Check dependency and dataset licences. Do not add paid APIs, hosted inference, cloud GPUs, subscriptions, or billing-triggering workflows without explicit approval.

## 7. Public reference guidance

- [NASA Systems Engineering Handbook](https://www.nasa.gov/reference/system-engineering-handbook-appendix/) — requirements, risk management, and verification/validation matrices.
- [NASA software engineering and assurance resources](https://www.nasa.gov/intelligent-systems-division/software-management-office/nasa-software-engineering-procedural-requirements-standards-and-related-resources/) — software lifecycle, assurance, and safety.
- [NASA-STD-8739.8B](https://standards.nasa.gov/standard/nasa/nasa-std-87398) — software assurance and software safety.

These are learning references; this independent project is not represented as NASA-compliant.
# PUI89 Automation Operating Standard

Applies to this repository and future PUI89 projects.

## Operating principles
- Automate repeatable software checks; keep consequential decisions under authorised human control.
- Reuse shared AI Core contracts and evidence formats. Avoid duplicate project-specific copies of common logic.
- Prefer local, standard-library checks and existing dependencies.
- No paid APIs, hosted inference, cloud GPUs, paid runners, subscriptions, automatic model/data downloads, or hardware actuation.
- No scheduled CI jobs or recurring network jobs by default. Keep CI event-driven (pull request, relevant push, manual dispatch).
- No automatic artifact uploads by default. Keep workflow permissions least-privilege and execution bounded.
- If cost, licence, privacy, or resource impact is uncertain, disable the feature pending review.

## Standard process
1. Intake: define goal, scope, assumptions, hazards, data sensitivity and cost constraints.
2. Baseline: record commit, environment, commands and existing test results.
3. Static checks: syntax and configuration; use lint/security tools only if already available and approved.
4. Contract checks: validate WorldState, Observation, ActionProposal and FailureReport.
5. Input integrity: reject malformed, missing, stale, conflicting, uncalibrated or provenance-free evidence.
6. Safety gate: fail closed on unknown or unsafe states; require human review for consequential actions; keep actuation disabled in software-only workflows.
7. Deterministic evaluation: use small fixed-seed scenarios, including success, failure, degraded inputs, communication loss and recovery.
8. Evidence report: record commit, command, environment, scenario, seed, counts, failures, limitations and relevant hashes.
9. Review/release: use protected branches and pull requests; merge only after required checks and review.
10. Post-change: compare against baseline, record regressions, unresolved risks and rollback steps.

## Shared contracts
- WorldState: time, context/frame, source references, quality, uncertainty, known and unknown fields.
- Observation: modality, provenance, timestamp, calibration/quality, payload reference and uncertainty.
- ActionProposal: proposed action, rationale, preconditions, risk, uncertainty, approval requirement and simulation-only state.
- FailureReport: failure, impact, evidence, containment, recovery recommendation and unresolved uncertainty.

Contracts must be versioned. Missing or conflicting evidence must never be silently guessed.

## Project-specific boundaries
- Coconut: dataset provenance/licence, annotation quality, leakage-resistant splits, maturity/localization evaluation, abstention and worker/animal safety.
- Flood Rescue: degraded sensors, communication loss, safe-hold proposals, route/scenario metrics; toy simulation is not flood-physics or rescue validation.
- Multimodal Screening: sensor provenance/calibration, missing or disagreeing modalities, error-rate reporting and authorised human review; RGB alone cannot establish chemical identity.
- Homeguard: stale/missing/uncalibrated inputs, baseline drift, evidence integrity and human-reviewed hazard escalation; software reports are not certified alarms or structural assessments.
- Future products (including AI Motorcycle) inherit these contracts before product-specific autonomy is added.

## Physical resilience and security
Water, dust, heat, fire, impact, vibration and electrical protection are design requirements until tested. Do not claim an IP rating or fire performance without appropriate physical testing. Threat-model dependencies, secrets, workflows, permissions, supply chain and update paths. Do not expose credentials or sensitive data in logs.

## Evidence labels
IMPLEMENTED = code/config exists.
TESTED = a named test ran and result is recorded.
MEASURED = reproducible metric on a documented evaluation set.
SIMULATION-ONLY = synthetic/simulated evidence only.
PROPOSED = planned work only.
NOT VALIDATED = real-world capability is unproven.

## Definition of done
A change is complete only when purpose, tests, evidence, limitations, cost impact, security impact and rollback path are documented. A green software test does not certify a physical robot, sensor, dataset or operational capability.

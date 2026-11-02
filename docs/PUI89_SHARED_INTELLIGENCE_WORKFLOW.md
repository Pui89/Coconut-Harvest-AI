# PUI89 Shared Intelligence Workflow v1.0

Common evidence-first workflow for all four existing PUI89 applications. This standardises reporting and safety gates; it does not claim every sensing, prediction, or robot capability is implemented.

## Common process
1. **Perceive** — accept available inputs and record source and timestamp.
2. **Understand** — construct a bounded world-state summary; do not fill gaps with guesses.
3. **Check evidence** — retain provenance, quality, review status, and limitations.
4. **Assess uncertainty** — record missing, stale, noisy, or conflicting information.
5. **Assess risk** — describe hazards, severity, and mitigations.
6. **Plan** — produce recommendations with evidence basis and approval requirements.
7. **Apply safety gate** — stop or require human review when evidence or safety conditions are insufficient.
8. **Execute or simulate** — proposals and simulation are not hardware execution.
9. **Verify** — compare outcomes with defined checks and preserve test evidence.
10. **Report and improve** — emit the shared report contract and record failures.

## Project-specific interpretation
- Coconut Harvest AI: maturity and harvest observations, tree and worker safety, collection plan.
- Flood Rescue AI: water and terrain state, people/animals/obstacles, route and mission risk.
- Multimodal Narcotics Screening AI: approved sensor evidence, anomaly review, privacy and human decision authority.
- Homeguard AI Nomad: indoor environment state, hazard observations, navigation and user-approved assistance.

## Evidence boundaries
Stages are `proposed`, `implemented`, `tested`, `simulated`, and `validated`. Passing software tests does not validate a model or field performance. Simulation does not establish real-world safety. A confidence value is not calibrated unless calibration evidence exists.

## Safety boundaries
- No unapproved hardware actuation.
- No autonomous enforcement, accusation, detention, or coercive action.
- Stop or request human review when inputs are missing, contradictory, stale, or outside tested limits.
- Minimise personal data and follow project privacy and retention rules.

Machine-readable contract: [schemas/pui89-intelligence-report.schema.json](../schemas/pui89-intelligence-report.schema.json).

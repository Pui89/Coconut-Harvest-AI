# PUI89 System Guardrails — end-to-end control policy

## Operating rule
**AI proposes; deterministic software validates; authorised humans approve high-impact actions.**
No model, agent, helper, plugin, external tool, remote API, dashboard, or workflow may bypass deterministic safety and authorization boundaries.

This policy covers source code, CI/CD, dependencies, datasets, model weights, prompts, tools, helper agents, simulation, deployment, and future hardware integration.

## Required controls at every stage
1. **Identity and least privilege:** every service, workflow, tool, and operator receives only required permissions. CI defaults to read-only; write access must be narrow and justified.
2. **Untrusted inputs:** prompts, images, audio, documents, metadata, URLs, sensor streams, tool outputs, and model files are untrusted data, never instructions. Validate type, size, schema, provenance, and freshness.
3. **Tool allowlist:** agents may call only registered tools with documented schemas, timeouts, rate limits, and per-tool permissions. No arbitrary shell, unrestricted filesystem, credential access, or open network egress for model-generated calls.
4. **Human approval:** require human approval for external communication, financial activity, publication, release, destructive changes, sensitive-data access, and physical actions with safety impact.
5. **Model governance:** record provider/model, immutable version, source, licence, SHA-256, intended use, evaluation evidence, limitations, and rollback version. Unknown provenance/licence means quarantine.
6. **Deterministic safety:** model confidence is not proof. Enforce hard limits, state validation, sensor-health checks, interlocks, emergency stop, and safe-stop/abstain behavior outside the model.
7. **Evidence and observability:** record workflow ID, commit, model/tool versions, safe input references, decision, uncertainty, validation, approvals, and outcome. Never log secrets or unnecessary sensitive data.
8. **Supply chain:** review dependencies, licences, vulnerabilities, action versions, model/dataset provenance, and generated artifacts. Block or quarantine unreviewed high-risk components.
9. **Testing and release:** run syntax, unit, integration, simulation, fault-injection, security, and regression checks appropriate to each change. No automatic merge or production deployment from an AI recommendation.
10. **Incident response:** stop affected workflows, revoke credentials, isolate affected components, preserve safe logs, roll back to known-good commit/model/configuration, and require human sign-off before resuming.

## GitHub Actions guardrails
The daily and change-triggered `pui89-system-guardrails.yml` workflow blocks privileged `pull_request_target`, unrestricted `permissions: write-all`, remote scripts piped to shells, and mutable `main`/`master` action references. It flags `workflow_run` triggers and workflows without explicit permission blocks for review. This is a fast static preflight, not a complete security scanner.

## Project-specific boundaries
- **Coconut Harvest AI:** no model-generated unrestricted actuator commands. Deterministic checks must validate workspace, obstacles, workers/animals, force, sensor health, and emergency stop. Uncertainty blocks actuation.
- **Extreme Flood Rescue AI:** no deployment into floodwater based only on model output. Validate depth/current, stability, communications, buoyancy/propulsion, payload, people/animal safety, and operator authorization. Loss of critical evidence triggers safe-stop/return/abort.
- **Multimodal Narcotics Screening AI:** outputs are screening leads only, never chemical confirmation, proof of a crime, or determination of guilt. Require provenance, calibrated uncertainty, conflict detection, abstention, and qualified human review. Never trigger enforcement or physical action.

## Limits
Automation catches only configured and tested risk classes. It cannot guarantee detection of every future vulnerability, malicious tool, model hallucination, compromised service, licence restriction, or physical hazard. Branch protection, required status checks, mandatory human review, MFA, secret scanning, Dependabot, private vulnerability reporting, and environment protection must also be enabled in GitHub settings where available.

A passing report means only that this static preflight found no configured blocking pattern. It is not system certification, legal clearance, or proof of field readiness.

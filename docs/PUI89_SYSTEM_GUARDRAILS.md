# PUI89 System Guardrails — end-to-end control policy

## Operating rule

**AI proposes; deterministic software validates; authorised humans approve high-impact actions.**
No model, agent, helper, plugin, external tool, remote API, dashboard, or workflow may bypass the project's deterministic safety and authorization boundaries.

This policy applies to source code, CI/CD, dependencies, datasets, model weights, prompts, tools, helper agents, simulation, deployment, and future hardware integration.

## Required controls at every stage

1. **Identity and least privilege** — every service, workflow, tool, and operator gets only the permissions required for its task. CI defaults to read-only; write permissions must be narrowly scoped and justified.
2. **Untrusted input boundary** — prompts, images, audio, documents, sensor messages, URLs, tool outputs, model files, and retrieved content are data, never trusted instructions. Validate type, size, schema, provenance, and freshness.
3. **Tool allowlist** — agents may call only explicitly registered tools with documented input/output schemas, timeouts, rate limits, and per-tool permissions. No arbitrary shell, unrestricted filesystem, credential access, or open network egress for model-generated tool calls.
4. **Human approval** — require a named human approval for external communication, financial activity, publication, release, destructive changes, sensitive-data access, and any physical action with safety impact.
5. **Model governance** — record model/provider, immutable version, source, licence, SHA-256, intended use, evaluation evidence, limitations, and rollback version. Unknown provenance or licence means quarantine; do not deploy by default.
6. **Deterministic safety supervisor** — model confidence is not a safety proof. Enforce hard limits, state validation, sensor-health checks, interlocks, emergency stop, and safe-stop/abstain behavior outside the model.
7. **Evidence and observability** — log workflow ID, commit, model/tool versions, inputs by safe reference, decision, confidence/uncertainty, validation result, approvals, and outcome. Never log secrets or unnecessary personal/sensitive data.
8. **Supply-chain controls** — review dependencies, licences, vulnerabilities, action versions, model/dataset provenance, and generated artifacts. Unknown, unreviewed, or high-risk components are blocked or quarantined.
9. **Testing and release** — run syntax, unit, integration, simulation, fault-injection, security, and regression checks appropriate to the change. A green CI run is not proof of field readiness. No automatic merge or production deployment from an AI recommendation.
10. **Incident response and recovery** — stop affected workflows, revoke credentials, isolate affected components, preserve safe logs, roll back to a known-good commit/model/configuration, and require human sign-off before resuming.

## GitHub Actions guardrails

The `pui89-system-guardrails.yml` workflow runs on pushes to main, pull requests, daily schedule, and manual dispatch. Its standard-library audit blocks:
- privileged `pull_request_target` triggers;
- unrestricted `permissions: write-all`;
- remote shell scripts piped directly from `curl` or `wget`;
- GitHub Actions references that track mutable `main` or `master` branches.

It reports workflows with missing explicit permission blocks and `workflow_run` triggers for human review. The audit is intentionally a fast static preflight, not a complete security scanner.

## Project-specific non-negotiable boundaries

- **Coconut Harvest AI:** no AI-generated unrestricted actuator commands; harvesting requires deterministic workspace, obstacle, worker/animal, force, sensor-health, and emergency-stop checks. If any safety precondition is uncertain, do not actuate.
- **Extreme Flood Rescue AI:** no autonomous deployment into floodwater based only on model output. Validate water depth/current, stability, communications, buoyancy/propulsion state, payload, people/animal safety, and rescue-operator authorization; safe-stop/return/abort on loss of critical evidence.
- **Multimodal Narcotics Screening AI:** outputs are screening leads only, never chemical confirmation, proof of a crime, or a determination of guilt. Require calibrated uncertainty, evidence provenance, conflict detection, abstention, and qualified human review. Never trigger enforcement or physical action.

## What automation can and cannot guarantee

Automation can detect configured classes of errors and enforce tested gates. It cannot guarantee that every future vulnerability, malicious tool, model hallucination, compromised external service, licence restriction, or physical hazard will be detected. It cannot independently configure every GitHub account/repository security setting. Branch protection, required status checks, mandatory human review, MFA, secret scanning, Dependabot, private vulnerability reporting, and environment protection must also be enabled in GitHub settings where available.

**Status must be evidence-based:** a passing guardrail report means only that this static preflight found no configured blocking pattern. It does not certify the system, models, robot, legal status, or commercial readiness.

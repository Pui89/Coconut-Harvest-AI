# Token-efficient engineering

**Policy:** Reduce unnecessary context and output; never reduce security, correctness, evidence, testing, human approval, or physical-safety controls. Zero-cost only.

## Required workflow

1. **Context pruning:** Load only task-relevant requirements, files, history, and constraints. Reuse concise authoritative project facts; remove duplicated or stale context without dropping safety-critical information.
2. **Targeted inspection:** Search first, inspect exact files/symbols and bounded line ranges, and expand only when evidence requires it. A narrow inspection must not replace a required full security or dependency audit.
3. **Diff-first validation:** Review changed files first, run the smallest relevant existing tests, then required regression/security checks. Tie every result to the exact commit SHA; never count stale, skipped, partial, or truncated checks as passing.

## Output discipline

- Report decision-relevant results, evidence links, exact paths/SHAs, uncertainty, risks, and next action.
- Summarise logs without discarding actionable failures or reproducibility evidence.
- Keep verified facts, estimates, proposals, and unknowns separate.
- Avoid repeating unchanged background or dumping entire files when a bounded excerpt is sufficient.

## Measurement

For comparable tasks, record input/output/cached tokens when the platform exposes them, context/files inspected, tests and security coverage retained, and rework. Calculate reduction only against a documented comparable baseline. If either measurement is missing, report **not measured**; never claim a 50–75% saving without evidence.

## Hard limits

No paid APIs, subscriptions, cloud GPUs, paid runners, metered services, new accounts, package installs, or model downloads without explicit approval. Do not suppress vulnerabilities, failed tests, licence/provenance checks, safety gates, uncertainty, or human review to save tokens. Cache only where already supported at no added cost and billing is verified.

## Project-specific guardrails

Retain this repository's domain-specific validation, safety boundaries, data rights, provenance, and human-approval requirements. A successful software test does not prove model accuracy, physical safety, field readiness, or certification.

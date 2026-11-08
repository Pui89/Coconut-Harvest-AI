---
name: context-pruning
description: Reduce unnecessary AI context by retaining only task-relevant requirements, decisions, evidence, and file excerpts. Use when a task has long history, repeated discussion, or large context.
---

# Context Pruning

## Procedure
1. State the requested outcome in one sentence.
2. Extract only constraints that can change the implementation: safety, compatibility, licensing, cost, scope, and acceptance criteria.
3. Keep the latest confirmed decision when earlier decisions conflict; preserve unresolved conflicts as open questions.
4. Replace long history with a compact working brief:
   - Goal
   - Must-preserve constraints
   - Relevant paths / interfaces
   - Known evidence and gaps
   - Acceptance checks
5. Do not repeat facts already present in the active context.
6. Retrieve additional history only when a missing decision materially affects correctness.

## Output budget
- Prefer a short checklist over narrative history.
- Quote source text only when exact wording matters.
- Keep summaries factual; distinguish confirmed facts from assumptions.
- Do not omit safety constraints merely to shorten context.

## Guardrails
- Never infer implementation or validation from a proposal.
- Never discard uncertainty, provenance, or human-approval requirements.
- Token savings are task-dependent; do not promise a percentage without measurement.

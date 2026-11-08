---
name: diff-first-validation
description: Implement changes as small reviewable diffs and validate only the affected behavior first. Use for coding, refactoring, documentation, and pull-request review.
---

# Diff-First Validation

## Procedure
1. Define the smallest acceptance criteria before editing.
2. Inspect current behavior and existing tests; avoid speculative rewrites.
3. Change the fewest files and lines that safely satisfy the criteria.
4. Review the diff immediately for unrelated edits, duplicated logic, secrets, unsafe defaults, and unsupported claims.
5. Run the narrowest relevant test or static check.
6. Expand validation only when the change crosses interfaces, safety boundaries, or shared contracts.
7. Report exact commands/checks and outcomes; list checks not run.

## Efficiency rules
- Reuse project tooling and installed dependencies.
- Do not install packages, download models, or call paid/hosted services for routine checks.
- Avoid repeating successful checks when inputs and code have not changed.
- Cache or reuse deterministic local results only when the project already has a safe mechanism.
- Do not weaken tests or skip required checks to make a change appear successful.

## PUI89 safety rules
- Keep perception, confidence, and action proposal separate.
- Preserve unknown/stale/conflicting evidence states.
- No physical robot actuation from an unvalidated proposal.
- Require human review for safety-critical or enforcement-related decisions.
- Label simulations, concepts, and unvalidated performance claims accurately.

## Completion report
Summarize: changed paths, behavior changed, checks run/results, remaining risks, and whether any cost or external service was introduced.

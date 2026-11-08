# PUI89 AI Engineering Instructions

Use the three repository skills in `.github/skills/` to keep AI-assisted work focused and economical.

## Operating rules
- Start from the user's requested outcome; do not reload unrelated project history.
- Inspect the smallest relevant file set. Search first; read bounded sections when possible.
- Reuse existing contracts, helpers, tests, and documentation before creating alternatives.
- Make the smallest safe diff. Do not rewrite whole files for a local change.
- Run focused checks first, then broader tests only when the change warrants them.
- Report changed files, checks actually run, results, remaining risks, and unverified assumptions.
- Never claim a test, benchmark, deployment, or token saving that was not measured.
- Do not introduce paid APIs, subscriptions, hosted model calls, cloud GPUs, or new dependencies without explicit approval.
- Prefer existing runtime and standard-library tools. Do not download model weights or install packages just to explore.
- Preserve human approval for safety-critical actions and keep robot actuation proposal-only unless the project explicitly validates otherwise.

## Skill selection
- Context/history is excessive: use `context-pruning`.
- Repository scope or relevant files are unclear: use `targeted-inspection`.
- Implementing, reviewing, or validating a change: use `diff-first-validation`.

These practices aim to reduce unnecessary prompt and tool usage. Savings vary by task and must be measured rather than assumed.

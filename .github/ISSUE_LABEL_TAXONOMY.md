# PUI89 Issue Label Taxonomy (proposed)

This file defines the shared label vocabulary for consistent triage. It does not create repository labels; repository metadata must be created separately.

| Label | Meaning |
|---|---|
| `type:bug` | Reproducible defect |
| `type:feature` | New capability or bounded engineering task |
| `type:security` | Security, privacy, or abuse concern |
| `type:docs` | Documentation-only change |
| `priority:high` | Time-sensitive or material safety/security/customer impact |
| `priority:normal` | Normal planned work |
| `status:blocked` | Cannot proceed until a dependency or decision is resolved |
| `evidence:required` | Work needs additional evidence before acceptance |

## Triage rules

- Apply one primary `type:` label.
- Apply one `priority:` label after impact review.
- Use `status:blocked` only while a concrete blocker exists.
- Use `evidence:required` when acceptance depends on missing tests, provenance, validation, or independent review.
- Do not use labels to imply implementation, testing, verification, certification, or deployment.
- Never place secrets, personal data, or sensitive operational details in public issues.

# PUI89 ZERO-LOSS AI OPERATION POLICY v0.1

**Applies to:** This repository and all AI-assisted work on its files, assets, documentation, data and configuration.
**Cost rule:** Zero-cost-first. No paid backup services or recurring commitments without explicit human approval.
**Status:** Mandatory policy; implementation and successful restore tests must be evidenced separately.

## Seven mandatory rules

1. **No automatic deletion:** AI must never automatically delete important files.
2. **No unprotected overwrite:** Never overwrite an original without first creating and verifying a recoverable copy.
3. **Change Preview before bulk edits:** Before changing multiple files, show exact paths and proposed additions, edits, moves and deletions. Stop for human review.
4. **Traceable changes:** Every modification must be reviewable and traceable to the task, actor/tool, timestamp, affected paths and before/after version identifiers.
5. **Human approval for permanent deletion:** Permanent deletion requires explicit human approval after backup verification. Prefer archive/quarantine first.
6. **Stop on uncertainty:** If target, scope, permissions, backup status or intended result is uncertain, stop and report. Never guess and proceed.
7. **Test recovery:** Test file-level and full-project restoration. Creating a backup alone does not prove recoverability.

## Required safe workflow

1. Inspect the repository, current branch/commit and exact task scope.
2. Identify protected originals and affected files.
3. Create a pre-change checkpoint and verify it can be read.
4. Produce a Change Preview before any bulk modification.
5. Obtain human approval for destructive, broad-scope or irreversible operations.
6. Make the smallest change on a separate branch or copy.
7. Review the diff; run relevant tests and integrity checks.
8. Keep the last known-good version until the new version is verified.
9. Record the change and recovery point.

## Recovery requirements

- Preserve Git history and known-good commits; do not treat Git history alone as an independent backup.
- Keep an independent backup outside the same repository/account/device failure boundary where feasible.
- Restore files or the entire project into a separate location first; do not overwrite the only remaining copy.
- Verify paths, file counts, checksums where available, metadata and project tests.
- Record restore date, source recovery point, test evidence, exclusions and unresolved risks.
- Mark controls **NOT TESTED** until an actual restore drill succeeds. Never claim guaranteed or zero-loss recovery without evidence.

## GitHub safeguards

Use protected default branches, reviewable pull requests, least-privilege access and secret scanning where available at no cost. Never put credentials or private data in public backups. Branch protection and GitHub commit history do not protect against every owner-level deletion, account loss or platform failure.

## Maturity labels

- **PROPOSED:** requirement documented, not implemented.
- **IMPLEMENTED:** control exists in code or configuration.
- **TESTED:** recorded test passed under stated conditions.
- **NOT TESTED:** no restore evidence exists.
- **LIMITED:** known exclusions or dependencies remain.

**Core rule: Never replace the last known-good copy with an unverified change.**

# Coconut Harvest AI — PUI89 Security Core Adoption Record

**Shared standard:** PUI89 Security Core Standard v0.1, proposed in [PUI89-Shared-AI-Core PR #13](https://github.com/Pui89/PUI89-Shared-AI-Core/pull/13). The shared standard is currently a draft and has not been merged.
**Project scope:** Agricultural robot concept; physical manipulation and worker/animal proximity create high-consequence hazards.
**Review date:** 2026-11-10
**Overall status:** IN PROGRESS — policy documentation exists; technical enforcement has not yet been independently verified.

## Control status

| Control area | Current evidence status | Required next verification |
|---|---|---|
| Repository ownership and collaborators | Unknown | Inspect collaborators, outside collaborators, GitHub Apps, deploy keys, webhooks and token scopes |
| Default-branch protection | Unknown | Inspect actual rulesets/branch protection, required reviews/checks, bypass actors, force-push and deletion controls |
| Contribution controls | Unknown | Verify pull-request requirements, review independence and untrusted-fork workflow boundaries |
| GitHub Actions | Unknown | Inspect workflow permissions, triggers, action SHA pins, runner type and secret exposure |
| Secrets | Unknown | Verify available secret scanning/push protection and inspect tracked files/history safely |
| Dependencies and supply chain | Unknown | Review manifests, lockfiles, licences, provenance and vulnerability evidence |
| Models, datasets and external tools | Unknown | Record publisher/owner, provenance, licence, telemetry, network destinations and permissions |
| Privacy and data handling | Unknown | Classify data, review public/private boundaries, retention and log minimisation |
| Backup and recovery | Unknown | Identify independent backup, integrity check and successful restore-test evidence |
| AI/agent and physical safety | Specified in project policy where applicable; implementation unknown | Verify fail-closed gates, human approval, safe-state boundaries and disabled-by-default execution |

## Project-specific risk boundary

Agricultural robot concept; physical manipulation and worker/animal proximity create high-consequence hazards.

AI outputs are advisory unless a separately reviewed and validated control system establishes otherwise. This record does not authorise physical actuation, enforcement, deployment, or changes to repository permissions.

## Required audit outputs

For every control, record one status: **Specified**, **Configured**, **Tested**, **Failed**, **Unknown**, or **Not applicable** (with reason). Attach evidence links and dates. Record findings, severity, containment recommendations, owner approval, remediation, and verification results.

## Zero-cost constraints

No paid API, subscription, cloud GPU, metered scanner, new package, model download, or external service is authorised by this record. If cost, data transfer, or billing behaviour is uncertain, stop and request owner approval.

## Recovery evidence

- Independent backup location / credential boundary: Unknown
- Backup integrity evidence: Unknown
- Last successful restore drill: Unknown
- Restored file and metadata verification: Unknown

Do not describe this repository as hardened or fully protected until relevant controls are configured and verified. A policy file or successful CI run alone is not proof of protection.

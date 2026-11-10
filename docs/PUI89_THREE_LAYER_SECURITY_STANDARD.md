# PUI89 Three-Layer Security Standard

Status: baseline policy and automated checks; not a certification or guarantee against compromise.
Applies to every PUI89 repository, software component, dataset, model artifact, simulation, and future project.

## 1. PUI89 Security Core — prevention and detection
- Treat external code, models, datasets, prompts, packages, and generated files as untrusted until reviewed.
- Prefer standard-library and already-installed tools. This baseline requires no paid APIs, subscriptions, cloud GPU, or extra package installation.
- Review dependency provenance, maintainer, release history, licence, and known vulnerabilities before adoption. Do not silently auto-upgrade.
- Never commit credentials, private keys, access tokens, personal data, or unapproved sensitive datasets. Never print secrets in logs.
- Validate inputs, file paths, model outputs, and tool/action proposals. Model output is data, not authority.
- Record uncertainty, source/provenance, validation status, and limitations. Fail closed for safety-critical or destructive actions.

## 2. PUI89 Repository Defense — integrity and change control
- Protect the default branch: require pull requests and passing checks where supported; block force-push and deletion; restrict bypass to the owner.
- Set workflow permissions to read-only by default. Grant write permissions only to a specific job that demonstrably needs them.
- Review workflow, dependency, binary/model, dataset, and safety-critical changes before merge. Never expose write tokens or secrets to untrusted pull-request code.
- Use CODEOWNERS where practical. Require human approval for security policy, workflows, release configuration, datasets, and safety-critical behavior.
- Do not enable auto-merge, auto-deployment, or destructive cleanup as a security shortcut.
- Review collaborators, GitHub Apps, and access tokens periodically. Enable account 2FA/passkeys and store recovery codes offline.
- Rulesets are one layer only: account compromise, repository-owner compromise, platform administrators, and external copies/backups are separate trust boundaries.

## 3. PUI89 Evidence & Recovery — auditability and restoration
- Preserve original datasets and released artifacts as immutable inputs; write derived outputs separately with version identifiers.
- Record commit SHA, UTC timestamp, tool/version, input identifiers or hashes, checks, result, and reviewer for security-sensitive changes.
- Keep an independent backup outside the active working copy. A Git remote alone is not an independent backup if the same account or credentials are compromised.
- Create a known-good restore point before risky changes. Test restoration of repository files and important data; record results and gaps.
- Never claim a backup is recoverable until a restore test succeeds. Never automatically delete or overwrite the last known-good copy.
- On suspected compromise: pause deployments and automation, preserve logs/commit references, rotate exposed credentials from a clean device, review collaborators/tokens/apps, restore from a verified clean point, and document the incident.

## Automated baseline
`.github/workflows/pui89-three-layer-security.yml` runs a local dependency-free repository hygiene check on pushes, pull requests, and manual dispatch. It does not exploit systems, upload repository contents, access secrets, or make network calls beyond GitHub checkout.

## Scope and limitations
These checks detect only a small set of high-confidence accidental exposures and policy regressions. They do not prove absence of malware, backdoors, zero-days, compromised dependencies, malicious maintainers, data exfiltration, or sophisticated obfuscation. They do not replace independent review, account security, rulesets, external backups, or incident response.

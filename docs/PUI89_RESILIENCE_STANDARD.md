# PUI89 Total Resilience & Intelligence Standard

**Applies to:** this repository, all PUI89 projects, and every future PUI89 project.  
**Policy:** zero-cost and local-first by default. No paid API, subscription, cloud GPU, or billable service without explicit owner approval.

## Mission: THINK · DO · FIND

- **THINK:** identify hazards, assess likelihood and impact, track uncertainty, compare safer options, and recommend the next useful action.
- **DO:** run permitted automated checks, enforce release gates, preserve evidence, and enter a safe state when a safety condition is violated.
- **FIND:** discover vulnerabilities, failure modes, missing evidence, suitable free/open tools, relevant standards, and funding/research opportunities.

## Required protection domains

Every project must assess and maintain a project-specific risk register for:

1. Cybersecurity: unauthorized access, credential exposure, malware, ransomware, malicious dependencies, prompt injection, data/model poisoning, and unsafe commands.
2. Water and environment: rain, immersion, humidity, condensation, dust, mud, corrosion, temperature, vibration, impact, and tampering.
3. Fire, heat, battery and electrical: overheating, short circuit, overcurrent, overvoltage, reverse polarity, battery damage, power loss, and thermal runaway.
4. Communications and positioning: network/signal loss, GPS denial, stale messages, sensor disconnection, interference, and clock/timestamp faults.
5. AI and data integrity: hallucinations, false predictions, bias, out-of-distribution inputs, uncertainty, calibration, missing/conflicting evidence, privacy, and provenance.
6. Mechanical and operational safety: jams, overload, instability, collision, unintended motion, actuator limits, emergency stop, and safe shutdown.
7. Human, mission and recovery safety: misuse, accidental activation, human review, mission abort, degraded operation, backups, incident response, and recovery.

## Mandatory engineering rules

- Treat every protection as **NOT VERIFIED** until supported by a suitable test and recorded evidence.
- Software checks cannot establish physical water, fire, impact, or ingress resistance.
- IP ratings (including IP67/IP68), flame ratings, temperature limits, load ratings, and safety claims are engineering targets only until the actual assembled equipment is tested by an appropriate method.
- Never claim a robot is waterproof, fireproof, floodproof, hack-proof, or safe for deployment without evidence.
- AI must not override independent hardware safety interlocks. Physical emergency stops, motor limits, fuses/BMS, and safe-state mechanisms must be designed and validated separately where applicable.
- For consequential screening or safety decisions, expose uncertainty and require qualified human review.
- Use least privilege, validate inputs, protect secrets, review dependencies and model licences, keep audit records, and prepare backup/restore and incident-response procedures.
- Do not introduce paid services or hidden usage charges. Prefer existing free GitHub capabilities and standard-library checks.

## Automated project gates

The repository workflow validates that this standard and a machine-readable project risk profile exist and that all protection domains are declared. Existing security workflows remain responsible for their existing code/dependency/security scans; avoid duplicating them here.

Before release, project owners must also review:
- relevant tests and simulation evidence;
- unresolved high-risk findings and safe failure behavior;
- hardware/environmental validation where physical resistance is claimed;
- human approval and operational limits;
- recovery and rollback readiness.

A passing policy workflow means the declarations are present and structurally valid. It does not mean physical resistance, cybersecurity, AI accuracy, or deployment safety has been proven.

## Required evidence record

For each material risk, record: hazard, affected component, likelihood, impact, mitigation, test method, result, evidence location, date/version, reviewer, and status (NOT_TESTED, PASS, FAIL, or NOT_APPLICABLE with rationale).

## New-project inheritance

Every new PUI89 repository must copy this standard, add .github/pui89-resilience.json with project-specific hazards, and include the pui89-resilience.yml policy workflow before its first release. The shared PUI89 AI Core should consume compatible risk/evidence reports across projects.

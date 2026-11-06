# PUI89 Total Resilience, SHIELD & Early Warning Standard

**Applies to:** all current and future PUI89 projects.  
**Operating policy:** strict zero-cost and local-first by default. No paid API, subscription, cloud GPU, billable service, or unapproved hardware purchase.

## Mission: THINK · DO · FIND

- **THINK:** identify hazards, assess likelihood and impact, track uncertainty, compare safer options, and prioritize risk reduction.
- **DO:** run permitted automated checks, enforce release gates, preserve evidence, and request project-specific safe-state behavior when a safety condition is violated.
- **FIND:** discover vulnerabilities, failure modes, missing evidence, suitable free/open tools, relevant standards, and research/funding opportunities.

## Required protection domains

Every project must maintain a project-specific risk register for all seven domains:

1. **Cybersecurity:** unauthorized access, credential exposure, malware, ransomware, malicious dependencies, prompt injection, data/model poisoning, unsafe commands, insecure updates and tampering.
2. **Water and environment:** rain, immersion, humidity, condensation, dust, mud, corrosion, temperature, vibration, impact and enclosure ingress.
3. **Fire, heat, battery and electrical:** overheating, short circuit, overcurrent, overvoltage, reverse polarity, battery damage, power loss, charging faults and thermal runaway.
4. **Communications and positioning:** network/signal loss, GPS denial or spoofing, stale messages, sensor disconnection, interference and clock/timestamp faults.
5. **AI and data integrity:** hallucinations, false predictions, bias, out-of-distribution inputs, uncertainty, calibration drift, missing/conflicting evidence, privacy and provenance.
6. **Mechanical and operational safety:** jams, overload, instability, collision, unintended motion, actuator limits, emergency stop and safe shutdown.
7. **Human, mission and recovery safety:** misuse, accidental activation, human review, mission abort, degraded operation, backups, incident response and recovery.

## PUI89 SHIELD architecture

SHIELD means **Safety, Hazard Intelligence, Emergency & Loss Defense**. It is a shared protection architecture integrated with the existing PUI89 Shared AI Core; it is not a second AI core and does not imply that physical sensors or safeguards already exist.

The common seven-stage workflow is:

1. **Observe and validate:** accept only identified inputs; retain sensor/source identity, timestamp, unit, quality and validity. Detect missing, stale, malformed, implausible, conflicting or tampered observations.
2. **Build WorldState:** form a bounded picture of the system and environment. Preserve unknowns; never turn missing data into a safe/normal reading.
3. **Assess hazard and uncertainty:** record hazard, affected component/person/mission, likelihood, severity, exposure, evidence, uncertainty and possible consequences.
4. **Classify warning:** use the common warning states below. Project-specific thresholds, persistence, hysteresis and combinations must be justified and tested; do not copy vehicle thresholds into other machines.
5. **Apply safety gate:** produce an ActionProposal with evidence, reason, risk, constraints and approval requirement. Reject proposals that exceed the project's verified operating envelope.
6. **Protect, notify and recover:** notify the responsible human and request the project-specific safe state. Critical hardware protections must be independent of AI/software where required. Recovery and reset require inspection and authorized human approval when risk warrants it.
7. **Verify and learn:** record outcomes, failures, false alarms, missed hazards, test configuration, software version and evidence. Use results to improve the risk register and benchmarks.

### Common warning states

- **NORMAL:** required observations are valid and within the tested envelope; continue monitoring.
- **ADVISORY:** early deviation or maintenance signal; record and inform the operator.
- **WARNING:** credible developing hazard; notify the operator and restrict affected non-essential proposals as defined by the project.
- **CRITICAL:** serious or imminent hazard; request the validated project-specific safe state and inhibit unsafe proposals. Do not assume software alone can physically stop a machine.
- **EMERGENCY:** emergency response is required; use independent hardware emergency-stop, isolation or protective devices where designed and validated, and notify the responsible human.
- **UNKNOWN / DEGRADED:** required data is missing, stale, contradictory, invalid or unavailable. Treat the affected function as not proven safe; enter its documented degraded/safe state or request human review.

A warning label is not a protective action. Alarm delivery, stopping, power isolation, braking, steering, door/valve control and other physical responses require separate hazard analysis, hardware design and validation. The safest response can differ by machine and operating condition; for example, abruptly stopping a moving vehicle may itself create danger.

### Minimum SHIELD event record

Every warning, fault or protective decision should preserve, where applicable:

- event identifier and schema version;
- project, component and operating mode;
- observation source/sensor identifier and timestamp;
- measured value, unit, validity and quality;
- evidence references and provenance;
- uncertainty and conflicting/missing inputs;
- hazard, severity and warning state;
- decision, rationale and proposed protective response;
- human approval/override requirement and outcome;
- software/configuration version, test reference and resolution.

## Shared AI Core contracts

All projects must reuse compatible definitions of:

- `WorldState` — bounded current system/environment state, including unknowns.
- `Observation` — source-attributed, timestamped and quality-checked input.
- `ActionProposal` — proposed action, rationale, evidence, risk, limits and authorization status; not a hardware command.
- `FailureReport` — fault, impact, evidence, uncertainty, safe-state outcome and recovery recommendation.

Evidence provenance, uncertainty, safety gates, human override, simulation/benchmark records, automated tests and security checks are common requirements. Vehicle- or robot-specific dynamics, thresholds, control logic and safety cases remain separate.

## Mandatory engineering rules

- Treat every protection as **NOT VERIFIED** until supported by a suitable test and recorded evidence.
- Software checks cannot establish physical water, fire, impact, ingress or battery resistance.
- IP ratings (including IP67/IP68), flame ratings, temperature limits, load ratings and safety claims are engineering targets until the actual assembled equipment is tested by an appropriate method.
- Never claim waterproof, fireproof, floodproof, hack-proof, autonomous-safe or deployment-ready without evidence.
- AI must not override independent hardware safety interlocks. Physical emergency stops, motor limits, fuses/BMS, isolation and safe-state mechanisms must be designed and validated separately where applicable.
- Consequential screening, rescue, home-safety and mobility decisions must expose uncertainty and preserve qualified human authority.
- Use least privilege, validate inputs, protect secrets, review dependencies and model licences, keep audit records, and prepare backup/restore and incident-response procedures.
- Do not introduce paid services or hidden usage charges. Prefer existing free GitHub capabilities and standard-library checks.
- No physical actuation, deployment or hardware test is authorized by this policy alone.

## Automated project gates

Each repository must validate that this standard, its machine-readable project risk profile and its SHIELD warning-system declaration exist and contain all required domains/states/fields. Existing security workflows remain responsible for their existing code, dependency and secret scans; avoid duplicating scans or adding paid services.

Before release, review:
- relevant tests and simulation evidence;
- missing/stale/conflicting sensor and communication-loss cases;
- false positives, missed hazards and warning delivery;
- unresolved high-risk findings and safe failure behavior;
- hardware/environmental validation where physical resistance is claimed;
- human approval, operating limits and emergency procedures;
- recovery, backup and rollback readiness.

A passing policy workflow validates declarations only. It does not certify physical resistance, cybersecurity, AI accuracy, sensor performance or deployment safety.

## Required evidence record

For each material risk, record: hazard, affected component, likelihood, impact, mitigation, test method, result, evidence location, date/version, reviewer and status (`NOT_TESTED`, `PASS`, `FAIL`, or `NOT_APPLICABLE` with rationale). Keep software, simulation, component, assembled-system and field evidence clearly distinguished.

## New-project inheritance

Every new PUI89 repository must inherit this standard, add `.github/pui89-resilience.json` with project-specific hazards and warning focus, and include the `pui89-resilience.yml` policy workflow before its first release. New projects must reuse the Shared AI Core contracts and SHIELD event format while maintaining their own hazard analysis, physical limits and validation evidence.

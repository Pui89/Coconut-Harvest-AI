# PUI89 SHIELD Project Implementation Matrix

**Status legend:** `POLICY_DEFINED` means requirements are documented; `SOFTWARE_REFERENCE` means dependency-free reference logic and tests exist on this development branch; `NOT_CREATED` means the project repository is not present in the connected Pui89 account. None of these statuses establishes physical validation.

## Shared requirements for all projects

- Reuse `WorldState`, `Observation`, `ActionProposal`, and `FailureReport` from the PUI89 Shared AI Core where already available.
- Preserve evidence provenance, timestamps, uncertainty, conflicting/missing input and calibration status.
- Use SHIELD warning states: `NORMAL`, `ADVISORY`, `WARNING`, `CRITICAL`, `EMERGENCY`, `UNKNOWN_DEGRADED`.
- Require safety gates and human review for consequential physical-action proposals.
- Keep AI outputs as proposals; no direct actuator command is introduced by the reference policy.
- Define project-specific safe states, operating envelopes, hazard thresholds and emergency procedures.
- Run unit, regression, security, simulation and benchmark checks; retain test configuration and evidence.
- Physical water/fire/battery/impact/functional safety and cybersecurity claims require suitable independent evidence.

## Project-by-project hazard and response matrix

| Project | Principal hazard focus | Safe-state design questions (must be answered and tested per project) | Current repository status |
|---|---|---|---|
| 01 Coconut Harvest AI | Worker/animal proximity, falling fruit, cutter and arm pinch/jam, dropped loads, tree/terrain stability, rain/moisture, battery and motor heat | Inhibit cutting when the safety envelope is uncertain; prevent uncontrolled arm/load motion; require local emergency stop and human recovery; never assume a sensor alone protects a worker | Existing repository; SHIELD branch prepared |
| 02 Flood Rescue AI | Water depth/current, capsizing, buoyancy, propulsion and retractable-wheel faults, ingress, battery isolation, tether/load limits, people/animal detection, communications/GPS loss | Define a tested flotation/degraded mode; avoid unsafe thrust or anchoring assumptions; preserve rescue-person safety and manual recovery; do not claim 0–15 m capability without structural and field evidence | Existing repository; SHIELD branch prepared |
| 03 Multimodal Screening AI | Sensor disagreement, calibration drift, false positives/negatives, adversarial inputs, data provenance, privacy, power/thermal faults | If evidence is incomplete or conflicting, return inconclusive and request qualified human review; never autonomously accuse, enforce, detain or take coercive action | Existing repository; SHIELD branch prepared |
| 04 Homeguard AI Nomad | Smoke/heat/fire, water leaks, electrical anomalies, stairs/falls, child/pet proximity, pinch points, tampering, privacy and network loss | Stop or park in a project-tested safe location; notify authorized users; preserve privacy; do not claim fire suppression or electrical protection unless actual hardware is installed and validated | Existing repository; SHIELD branch prepared |
| 05 AI Robot Car | Pedestrians/cyclists, collision, braking/steering faults, tire and stability faults, road/weather conditions, battery thermal events, sensor/GPS spoofing, communication loss, driver override | Define a vehicle-specific minimal-risk condition; avoid sudden-stop assumptions; maintain driver override and independent braking/steering/battery safeguards; no autonomous road operation before formal validation | **Repository not found / not created** |
| 06 AI Robot Motorcycle | Rider fall, lean-angle and balance dynamics, traction/wheel slip, braking, road users, blind spots, battery/thermal events, sensor faults, rider override | Prioritize rider stability; never issue unvalidated steering/braking/torque commands; define rider override and independently validated emergency behavior; start with rider-assistance research, not full autonomy | **Repository not found / not created** |

## Minimum validation layers

1. **Contract/unit tests:** schemas, missing/stale/conflicting inputs, warning-state precedence, evidence references and human-approval flags.
2. **Software integration tests:** sensor adapters, stale-message rejection, logging, privacy and permission boundaries.
3. **Simulation:** project-specific hazard scenarios with fixed seeds, model/version capture, expected outcomes and repeatable metrics.
4. **Component bench tests:** only when suitable equipment and safe facilities exist; document calibration and test limits.
5. **Assembled-system / field validation:** separate approval, hazard analysis, competent supervision and appropriate independent assessment.

## Shared benchmark record

For every scenario, record: scenario ID, project, hazard, initial state, injected fault, expected warning, expected safe-state proposal, actual result, false alarm/missed hazard, latency, evidence references, software/configuration version, random seed (if simulated), limitations and reviewer.

Do not combine simulation success with physical validation. Do not invent thresholds. Thresholds must come from the project hazard analysis, component specifications and appropriate standards.

## Next implementation actions

- Keep the common warning policy and contract tests in sync across the existing repositories until a separately governed shared-core package is established.
- Add project-specific scenario tests before enabling any physical response.
- Review existing repository workflows and security checks; avoid duplicate paid scans or new services.
- Create the Car and Motorcycle repositories only when repository creation is explicitly available/authorized; apply this standard from their first commit.

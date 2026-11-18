# PUI89 SHIELD Project Implementation Matrix

**Status legend:** Repository existence and documented software evidence do not establish physical validation. Each product README is the source for its current implementation and evidence stage.

## Shared requirements for all six products

- Reuse `WorldState`, `Observation`, `ActionProposal`, and `FailureReport` from PUI89 Shared AI Core where adopted.
- Preserve evidence provenance, timestamps, uncertainty, missing/conflicting input and calibration status.
- Use explicit warning states: `NORMAL`, `ADVISORY`, `WARNING`, `CRITICAL`, `EMERGENCY`, and `UNKNOWN_DEGRADED`.
- Require safety gates and human review for consequential physical-action proposals.
- Keep AI outputs advisory; do not create direct actuator control without separate engineering, validation and authorization.
- Define product-specific operating envelopes, safe states, hazard thresholds and recovery procedures.
- Run reproducible unit, contract, regression, security and simulation tests; retain evidence.
- Physical water/fire/battery/impact/functional safety and cybersecurity claims require suitable independent evidence.

## Product-by-product hazard and response matrix

| Product | Principal hazard focus | Safe-state design questions | Evidence boundary |
|---|---|---|---|
| **Coconut Harvest AI** | Worker/animal proximity, falling fruit, cutter/arm pinch or jam, dropped loads, tree/terrain stability, rain/moisture, battery and motor heat | Inhibit cutting when the safety envelope is uncertain; prevent uncontrolled arm/load motion; require emergency stop and human recovery | Software and evaluation preparation do not establish detector accuracy or physical harvesting capability |
| **PUI89 Sentinel** | Quadruped gait/fall risk, terrain and obstacle uncertainty, confined-space access, sensor disagreement, communications loss and recovery | Define mission-specific no-go conditions, safe hold, operator-controlled retreat and calibrated atmosphere checks where required | Four-legged inspection concept and requirements; no physical prototype or field capability is claimed |
| **PUI89 AI HOME** | Indoor fire/smoke, electrical and water hazards, stairs/falls, child/pet proximity, false alarms, privacy and offline operation | Define safe stop/park behaviour, reliable escalation, privacy limits and safe charging | Indoor assistance concept/software; no validated home-safety performance is claimed |
| **PUI89 AI NOMAD** | Four-wheel stability, tip-over, obstacle contact, motor/pinch hazards, payload restraint, battery/thermal faults and communications loss | Define payload limits, stability checks, safe stop and user-controlled recovery | Ground-based mobile assistant concept; physical mobility and payload performance remain unvalidated |
| **PUI89 AI Global SUV** | Collision exposure, vulnerable road users, road/weather/water uncertainty, driver distraction and vehicle electrical/thermal hazards | Keep advice separate from vehicle control; preserve driver authority and independent vehicle safety systems | SUV design and software concept; no vehicle integration, road test or certification is claimed |
| **PUI89 AI Step-Through Scooter** | Rider stability, traction, braking context, road users, weather/visibility and road-water uncertainty | Prioritize rider control; unknown water/road conditions must not be presented as safe; no autonomous steering, throttle or braking | Step-through scooter concept; no functioning scooter, rider trial or road certification is claimed |

## Minimum validation layers

1. **Contract/unit tests:** schemas, missing/stale/conflicting inputs, warning-state precedence, evidence references and human-approval flags.
2. **Software integration tests:** sensor adapters, stale-message rejection, logging, privacy and permission boundaries.
3. **Simulation:** product-specific hazard scenarios with fixed seeds, model/version capture, expected outcomes and repeatable metrics.
4. **Component bench tests:** only when suitable equipment and safe facilities exist; document calibration and test limits.
5. **Assembled-system / field validation:** separate approval, hazard analysis, competent supervision and appropriate independent assessment.

## Shared benchmark record

For every scenario, record: scenario ID, product, hazard, initial state, injected fault, expected warning, expected safe-state proposal, actual result, false alarm/missed hazard, latency, evidence references, software/configuration version, random seed (if simulated), limitations and reviewer.

Do not combine simulation success with physical validation. Do not invent thresholds. Thresholds must come from the product hazard analysis, component specifications and appropriate standards.

## Next implementation actions

- Keep common warning policies and contract tests aligned across the six product repositories.
- Add product-specific scenario tests before enabling any physical response.
- Review existing workflows and security checks; avoid duplicate paid scans or new services.
- Preserve human authority, open-source-first technology governance and evidence-led release gates.

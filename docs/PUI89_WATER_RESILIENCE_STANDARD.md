# PUI89 Water & Environmental Resilience Standard

**Status: SOFTWARE REQUIREMENTS / SIMULATION ONLY. Physical protection is not yet verified.**

## Purpose
Apply one reusable water-ingress monitoring and fail-safe software contract across PUI89 projects. The standard is local-first, Python-standard-library-only and requires no paid API, cloud GPU, model download, external service or hardware connection.

## Required physical design areas
1. Sealed enclosure with correctly selected gasket/O-ring, controlled compression and serviceable joints.
2. Sealed cable glands and connectors; protect every penetration, shaft and removable panel.
3. Water-compatible motors, bearings, actuators and propulsion components appropriate to the actual exposure.
4. Protected battery compartment, BMS, fuse/over-current protection and independently engineered isolation.
5. Corrosion-compatible materials, coatings and fasteners for the actual water chemistry.
6. Drainage/condensation strategy that does not create an ingress path; pressure equalisation only with suitably rated membranes.
7. Project-specific buoyancy, stability, propeller guards and current/depth limits where applicable.

## Software monitoring contract
- Monitor enclosure leak state, internal humidity, electronics temperature and battery health where sensors are actually integrated.
- Treat missing, stale, invalid or contradictory sensor readings as a fault; never interpret missing data as dry/safe.
- On confirmed ingress: raise a critical alert, request a safe stop, inhibit non-essential actuation and request human intervention.
- Do not automatically energise wet electronics, open compartments, restart motors or attempt recovery unless a separately engineered and tested safety case authorises it.
- Record timestamp, sensor identity, validity, observed value, threshold, decision, software version and evidence provenance.
- Preserve human authority for recovery and high-risk actions.

## Verification gates
- **Gate A — software:** deterministic simulated scenarios and automated CI checks.
- **Gate B — component:** supplier specifications for enclosure, connectors, motors, battery and sensors.
- **Gate C — assembly:** test the complete assembled robot, including seams, cable entries, shafts and service panels.
- **Gate D — field envelope:** controlled tests at declared water depth, duration, temperature, contamination and flow/current conditions.
- Publish only the exact tested configuration, depth, duration and conditions. IP67/IP68 labels are not a substitute for system-level testing; IPX8 conditions must be specified by the manufacturer/test agreement.

## Claims policy
This repository's software checks do **not** prove waterproofing, an IP rating, immersion survival, corrosion life, battery safety, buoyancy, stability or flood-current resistance. Until physical evidence is reviewed, report **NOT PHYSICALLY VALIDATED** and make no waterproof-performance claim.

## Project-specific envelope
See `.pui89/water_resilience.json` for the project's intended exposure and required monitoring signals. These are engineering requirements, not proof that hardware exists.

# Coconut-tree height feasibility and harvest-success criteria (0–30 m)

## Purpose

The 0–30 m range is the orchard/tree-height envelope for research planning, **not** a claim that the current robot can reach or harvest every height. The repository's concept illustrations are not photos of a built machine. A vision model may detect fruit at heights that the robot cannot safely access.

## Concept architecture requirements — design only

The system-level concept should compare a **slim telescopic mast/arm with a sensor head** against specialist access methods. A tracked or wheeled mobile base is only a candidate architecture; a ground base with a short arm must not be represented as reaching a tall crown. The intended 0–30 m tree-height envelope is a feasibility/design challenge, not a demonstrated mechanism reach.

| ID | Requirement | Evidence needed before the requirement can be called verified | Current status |
|---|---|---|---|
| ORCH-01 | Estimate tree height and each target fruit's 3D location, including uncertainty, calibration and timestamp/freshness. | Labelled held-out data for perception/localization; independent pose ground truth; error distribution by distance, occlusion and lighting. | Not measured for a representative real-orchard set. |
| ORCH-02 | Plan staged reach using a slim telescopic mast/arm and sensor head only within a separately verified mechanical envelope. | Defined geometry, joint/extension limits, load and deflection analysis, braking/retention, repeatable simulation and staged instrumented tests. | Concept only; dimensions, load capacity and safe reach are unknown. |
| ORCH-03 | Compare tracked and wheeled base options against orchard terrain and stability constraints. | Measured soil/slope/obstacle envelope, centre-of-mass and tip-risk analysis, stopping/holding tests, and recovery plan. | Not measured; no terrain or slope limits are claimed. |
| ORCH-04 | Use RGB perception first; use depth and/or LiDAR only when installed, calibrated, healthy and mutually consistent. | Tests for missing, stale, miscalibrated, obstructed and contradictory sensor data; conservative abstention on failure. | Optional sensor concept; no validated sensor-fusion claim. |
| ORCH-05 | Control fruit after detachment with an engineered capture/retention or lowering method; do not allow an uncontrolled fall. | Verified capture-state sensing, retention/load analysis, controlled drop/failure tests in a safe test fixture, and damage/drop logs. | Concept only; no capture hardware validated. |
| ORCH-06 | Select fruit using a maturity policy supported by labelled evaluation data; abstain on ambiguous or occluded cases. | Held-out per-stage precision/recall/F1 or confusion matrix, label QA, uncertainty and abstention tests. | Real-world maturity performance not established. |
| ORCH-07 | Enforce exclusion zones for people/animals, overhead lines, fronds/structures, collision hazards, wind and unstable ground. | Scenario tests plus an independently reviewed site-risk assessment; environmental operating limits measured for the actual design. | Requirements only; numerical wind/terrain limits are unknown. |
| ORCH-08 | Do not cut if perception, localization, reachability, stability, collision clearance, sensor health, capture readiness, communication or emergency-stop status is missing, stale, contradictory or uncertain. | Negative/fault-injection tests and independent hardware interlocks; human approval alone must never bypass a failed safety gate. | Software checks can be tested; physical interlocks and the complete chain are unverified. |

### Verification and validation checklist

- **Software verification:** test invalid/NaN/Inf coordinates and confidence, stale timestamps, missing or disagreeing sensors, unreachable targets, collision flags, uncertain maturity, unready capture, communications loss and emergency-stop inputs. Every unsafe or unknown state must resolve to `SURVEY_ONLY`, `SAFE_HOLD` or `ABORT_NO_CUT`, never a cut authorization.
- **Simulation verification:** use deterministic scenarios for each height band, localization uncertainty, occlusion, obstacle/overhead-line exclusion zones, unstable-ground assumptions, changing wind inputs, staged extension and capture failure. Report scenario count and failures; simulation is not physical proof.
- **Physical validation:** before any cutting or elevated operation, require independent mechanical/safety review, a guarded non-cutting test fixture, rated secondary retention, independent emergency-stop and power isolation, instrumented low-height tests, and a documented recovery plan. Do not test above people. High-height operation requires specialist feasibility review and staged evidence before trials.
- **Evidence reporting:** label every result as recorded-image evaluation, simulation, or physical hardware. Record commit, command, versions, environment, scenario/data split, sample count, measurements, failures and limitations. If a measurement or acceptance threshold is not defined or available, mark it **not measured** rather than estimating it.

## Height bands and evidence gates

| Target height | Candidate method to investigate | Current claim | Required gate before cutting |
|---|---|---|---|
| 0–3 m | Ground-level guarded tool / controlled test fixture | First candidate band for supervised non-cutting tests; no validated harvest-success claim | Calibrated reach and pose, guarded tool, independent stop, controlled capture, risk assessment |
| 3–6 m | Engineered extension mast or rated lift/platform | Feasibility only | Stability under full load, wind envelope, structural margin, collision checks, safe exclusion zone and repeatable physical tests |
| 6–12 m | Purpose-built high-reach or climbing mechanism | Research concept; not demonstrated by the compact pictured base | Rated load path, independent retention/braking, recovery plan, fall protection, full risk review and supervised subsystem tests |
| 12–20 m | Specialized tall-palm access/harvesting solution | Unvalidated | Independent engineering review and staged tests; no autonomous cutting until all safety and success gates pass |
| 20–30 m | Specialized tall-palm solution or alternate method | Outside current demonstrated capability | Feasibility study, access-method comparison, redundant retention and extensive validation; do not imply present capability |

The bands are planning categories, not universal engineering limits. Actual feasibility depends on palm geometry, trunk diameter, canopy shape, terrain, wind, payload, reach envelope, fruit mass, mechanism design and local safety rules. A compact ground robot with a short arm must never be described as reaching a 20–30 m crown.

## Per-tree workflow

1. **Survey:** capture RGB and, when available and calibrated, depth/LiDAR; identify the palm and estimate target height with uncertainty.
2. **Per-fruit assessment:** detect each coconut separately, retain the proposed class and confidence, and abstain on ambiguous maturity or occlusion.
3. **Reachability gate:** verify 3D target pose, actual mechanism envelope, joint limits, stability, collision clearance, sensor freshness and safe approach/retreat.
4. **Site/safety gate:** check people and animals, exclusion zone, falling-fruit path, wind/environmental limits, emergency stop, communications and independent retention where required.
5. **Operator confirmation:** early prototypes require explicit approval; class selection never bypasses reach or safety gates.
6. **Cut and capture only after approval:** use a guarded, validated tool and a controlled fruit path. If any prerequisite is unknown or false, return SURVEY_ONLY or ABORT_NO_CUT.
7. **Verify and log:** confirm detachment and safe capture/control using independent evidence or operator review. Log failures and near misses as well as successes.

## Definition of harvest success

Count one success only when the intended fruit is correctly selected, detached without an unsafe event, and safely captured or otherwise controlled, with the outcome verified and logged. Do not count any of these as success: detection alone, a planned trajectory, a simulated animation reported as physical operation, a cut without capture, or an unverified result.

Report, separately by height band and fruit stage:

- number of attempted tasks and number of verified successful harvests;
- successful harvest/capture rate and confidence interval;
- fruit selection errors, fruit damage, drops, aborts and recoveries;
- collision/near-miss and unsafe-action counts (target: zero; report the denominator);
- detection precision/recall, maturity confusion matrix, 3D localization error and reachability false-safe rate;
- cycle time and resource use, with environmental conditions and failure cases;
- evidence type: **recorded-image evaluation**, **simulation**, or **physical hardware**.

Do not publish a success percentage until the dataset/test protocol is frozen, the denominator and failures are available, and the results can be reproduced. Report simulation and physical results separately.

## Stop conditions

Stop without cutting if height/pose uncertainty is excessive, target is outside the verified reach envelope, the palm/robot is unstable, a collision-free path is unavailable, people/animals enter the exclusion zone, wind exceeds the validated limit, a required sensor/transform is stale or missing, retention/brake/communications fail, or the operator has not approved the task.

## Current status

This document is a feasibility and acceptance plan. It does not claim that any height band has passed physical harvesting tests. The current compact robot artwork is conceptual; real-world success requires a built mechanism, safety review, staged validation and published measurements.

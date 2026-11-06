# PUI89 SHIELD ↔ Shared AI Core Integration Contract

**Status:** architecture mapping documented; runtime wiring is `DESIGN_ONLY_NOT_CONNECTED` until project adapters and integration tests are implemented.  
**Purpose:** connect SHIELD to the existing PUI89 Shared AI Core without creating a second AI Core.

## Contract mapping

| Shared AI Core contract | SHIELD responsibility | Required behavior |
|---|---|---|
| `Observation` | Sensor/event intake | Preserve source ID, timestamp, unit, validity, quality, calibration state and evidence provenance. Reject or mark stale/missing/conflicting inputs. |
| `WorldState` | Current hazard picture | Represent known conditions, unknowns, affected component, operating mode and current warning state. Never infer safe/normal from missing data. |
| `ActionProposal` | Protective response proposal | Include rationale, evidence references, uncertainty, severity, constraints and human-approval requirement. It is not an actuator command. |
| `FailureReport` | Incident/fault record | Record trigger, affected system, impact, warning transitions, evidence, safe-state outcome, recovery recommendation and unresolved risk. |

## SHIELD event lifecycle

1. Convert each sensor or software signal into a provenance-bearing `Observation`.
2. Update the project-specific `WorldState` without discarding unknown or conflicting information.
3. Evaluate the project hazard rules and the common SHIELD warning-state vocabulary.
4. Emit a traceable SHIELD event using `schemas/pui89-shield-event.schema.json` (or the documented equivalent filename).
5. If a response is appropriate, create an `ActionProposal` with approval requirements and project-specific constraints.
6. Record rejected proposals, degraded operation and incidents through `FailureReport`.
7. Preserve benchmark/test references and the exact software/configuration version.

## Required safety boundaries

- SHIELD classification code is reference policy only; it does not acquire sensors or operate actuators.
- Project-specific hazard thresholds, safe states and emergency actions must not be copied between machines without hazard analysis.
- Independent hardware interlocks and protective devices remain necessary where required by the safety case.
- Physical action proposals require human review until a separately validated safety architecture establishes otherwise.
- Unknown, stale or conflicting observations must not produce a normal/safe conclusion.
- Screening decisions remain qualified-human-reviewed and non-coercive.
- No physical test, deployment or hardware action is authorized by this document.

## Integration acceptance criteria

- [ ] Existing Shared AI Core contracts are reused; no parallel contract family is introduced.
- [ ] SHIELD events map to `Observation`, `WorldState`, `ActionProposal` and `FailureReport`.
- [ ] Provenance, timestamps, uncertainty and missing/conflicting inputs survive the full path.
- [ ] Safety gate rejects proposals outside the project's verified operating envelope.
- [ ] Human override and incident recovery paths have project-specific tests.
- [ ] Simulation/benchmark records are reproducible and distinguish simulation from physical evidence.
- [ ] Project adapter tests pass before runtime integration is described as implemented.

## Current implementation truth

The current development branch contains the shared SHIELD policy reference module, event schema, scenario catalog, tests and this mapping document. The complete runtime adapter path is **not yet connected or verified**. No physical safety capability is claimed.

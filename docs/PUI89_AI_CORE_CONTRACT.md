# PUI89 AI Core Contract

**Status:** shared engineering contract for simulation and software tests; not a certification or claim of field readiness.

This contract keeps the three PUI89 AI application projects aligned while each project retains its domain-specific logic.

## 1. Required world-state safety signals

Every action proposal must receive explicit Boolean values for all four signals below. Missing, malformed, or unknown values must fail closed to `SAFE_HOLD`.

| Field | Safe-to-proceed value | Fail-safe condition |
|---|---|---|
| `emergency_stop` | `false` | `true`, missing, or not Boolean |
| `sensors_ok` | `true` | `false`, missing, or not Boolean |
| `sensor_data_fresh` | `true` | `false`, missing, or not Boolean |
| `comms_ok` | `true` | `false`, missing, or not Boolean |

Do not silently coerce strings such as `"false"`, integers such as `1`, or null values into Booleans.

## 2. Perception uncertainty

- Confidence must be a finite numeric value in the interval [0, 1]; Boolean values are not numeric confidence.
- Missing, malformed, out-of-range, or non-finite confidence must result in abstention (for example, `UNKNOWN`) rather than an affirmative detection.
- Conflicting modalities or missing required modalities must be represented explicitly and must not be hidden by a single confidence score.
- Project-specific thresholds must be documented and evaluated against labeled test data before any performance claim.

## 3. Human review and action boundary

- These autonomy-lab interfaces generate proposals and simulation labels only; they do not authorize hardware actuation.
- High-impact decisions must request human review. For narcotics screening, visual or multimodal screening is not chemical confirmation and must not independently accuse, detain, or penalize a person.
- A simulation scenario passing is not evidence of real-world safety, accuracy, rescue capability, or harvest capability.

## 4. Reproducible scenario reports

Automated scenarios should record the scenario identifier, seed where applicable, engine/version, input state, proposed action, decision trace, expected action, pass/fail outcome, and whether hardware actuation occurred. Reports should be deterministic for identical inputs where the implementation supports it.

At minimum, regression tests should cover:
- each required safety field missing or malformed;
- emergency stop, sensor failure, stale data, and communication loss;
- recovery after a fault clears;
- invalid confidence and conflicting/missing modalities;
- human-review gates for high-impact actions;
- stable report identifiers and an explicit no-hardware-actuation assertion.

## 5. Project-specific extensions

- **Coconut Harvest AI:** maturity-stage uncertainty, cutting/capture hazards, drop zone, and worker/animal separation.
- **Extreme Flood Rescue AI:** water/environment uncertainty, victim-location confidence, communication degradation, and simulation-only depth scenarios.
- **Multimodal Narcotics Screening AI:** sensor provenance, modality disagreement, chain of custody, instrument validation, and mandatory qualified human review.

## 6. Release gate

Before merging a change that affects the shared interface:
1. run the project regression tests and shared-interface smoke checks;
2. review failure reports rather than relying only on a green summary;
3. document untested assumptions and limitations;
4. keep model downloads, package installs, cloud services, and hardware actuation disabled unless separately approved and assessed.

**No measured results should be advertised unless they are reproducible and the dataset, split strategy, metric definition, and test conditions are recorded.**

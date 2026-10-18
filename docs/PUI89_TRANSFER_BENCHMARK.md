# PUI89 Cross-Environment Transfer Benchmark

## Research question

Can one embodied-AI architecture transfer its perception, world-model, uncertainty and planning capabilities between materially different environments without unsafe behavior?

## Domains

1. Agriculture — coconut orchard.
2. Disaster response — flood environment.
3. Security/inspection — industrial or logistics environment.

## Transfer matrix

| Train / develop | Evaluate | Required result |
|---|---|---|
| Agriculture | Disaster | quantify transfer and failure modes |
| Agriculture | Security | quantify transfer and failure modes |
| Disaster | Agriculture | quantify transfer and failure modes |
| Disaster | Security | quantify transfer and failure modes |
| Security | Agriculture | quantify transfer and failure modes |
| Security | Disaster | quantify transfer and failure modes |
| Joint / foundation | held-out domain | test generalization |

## Shared representation

Each domain should expose a common schema:

`Observation → Evidence → Object → Geometry → State → Uncertainty → Action proposal → Safety decision`

Domain-specific labels may differ, but the interface must remain stable.

## Metrics

- zero-shot transfer;
- few-shot adaptation;
- fine-tuning efficiency;
- performance degradation from source to target;
- calibration degradation;
- OOD detection;
- abstention quality;
- sensor-failure recovery;
- planning success;
- safety-gate rejection of unsafe proposals.

## Critical rule

A transferred model must **not** inherit authority merely because it performed well in another domain. Every deployment domain requires independent validation of perception, uncertainty, planning and safety.

## Benchmark protocol

1. Freeze source-domain training.
2. Freeze model/configuration.
3. Evaluate on target-domain held-out data.
4. Record all sensor and compute configurations.
5. Measure accuracy, latency and uncertainty.
6. Inject OOD and sensor-failure cases.
7. Measure safe abstention and safety-gate behavior.
8. Compare against domain-specific baseline.
9. Publish failure cases, not only aggregate scores.

## PhD value

This benchmark turns the three projects into controlled experiments for **cross-domain embodied intelligence**, rather than three unrelated applications.

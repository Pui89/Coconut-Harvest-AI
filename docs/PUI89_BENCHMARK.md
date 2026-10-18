# PUI89 Benchmark

This benchmark defines the minimum evidence required before this project is described as field-validated.

## Benchmark principles

- Every result has a dataset/version identifier.
- Every result records hardware and model versions.
- Targets are never reported as achieved results.
- Test and training data are separated.
- Failure cases are retained.
- Unknown/OOD cases are evaluated explicitly.
- Safety metrics are reported separately from AI accuracy.

## Core benchmark

| Perception | Coconut/tree detection AP, ripeness F1 |
| 3D | target localization error (cm), reachability precision |
| Planning | collision-free plan rate, planning latency |
| Manipulation | harvest success rate, fruit damage rate |
| Operations | coconuts/hour, trees/hour, energy/tree, uptime |
| Robustness | rain/low-light/occlusion/OOD/failed-sensor recovery |
| Safety | safety-gate intervention rate, E-stop verification, unsafe-command rejection |

## Required scenarios

- normal operating conditions;
- low light;
- rain/wet surfaces where relevant;
- occlusion;
- motion blur;
- sensor dropout;
- calibration error;
- communication loss;
- low battery;
- unexpected objects;
- out-of-distribution environment;
- conflicting sensor evidence;
- human intervention;
- emergency stop.

## Reporting template

For each experiment record:

```text
experiment_id
date
domain
dataset_version
hardware
sensor_configuration
model_version
software_commit
environment
scenario
metrics
confidence
uncertainty
OOD_score
failures
safety_events
human_interventions
result
limitations
```

## Publication rule

A claim is not a benchmark result until it has:
1. a defined protocol;
2. reproducible configuration;
3. measured data;
4. comparison baseline;
5. limitations;
6. recorded failure cases.


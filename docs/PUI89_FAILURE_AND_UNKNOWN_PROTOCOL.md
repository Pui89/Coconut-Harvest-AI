# PUI89 Failure, OOD and UNKNOWN Protocol

A professional autonomous robot must be able to refuse an unsafe or unsupported decision.

## Decision states

```text
EXECUTE
SLOW_DOWN
COLLECT_MORE_DATA
HUMAN_REVIEW
ABORT
UNKNOWN
```

## Inputs to the decision

- model confidence;
- calibrated uncertainty;
- OOD score;
- sensor health;
- cross-modal agreement;
- world-model consistency;
- task risk;
- robot state;
- communication state.

## Sensor failure

When a required modality fails:
1. mark the modality unavailable;
2. do not silently substitute fabricated values;
3. recompute evidence quality;
4. downgrade confidence;
5. switch to a validated degraded mode or UNKNOWN;
6. notify the operator;
7. log the event.

## OOD behavior

An OOD observation must not be converted into a high-confidence in-domain label solely because the classifier produces a high softmax score.

## Safety boundary

Foundation models can propose high-level interpretations or plans. They cannot bypass deterministic safety validation or directly control actuators.

## Required tests

Inject:
- missing RGB;
- missing depth;
- missing thermal;
- missing LiDAR;
- time synchronization drift;
- calibration drift;
- contradictory sensors;
- network loss;
- compute overload;
- stale model;
- unexpected geometry.

Success means the robot responds according to the validated safe policy, not merely that the AI classifier remains accurate.

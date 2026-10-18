# PUI89 MLOps and Model Lifecycle

## Lifecycle

```text
Dataset
  ↓
Version
  ↓
Training
  ↓
Validation
  ↓
Robustness / OOD
  ↓
Calibration
  ↓
Safety evaluation
  ↓
Approval
  ↓
Deployment
  ↓
Monitoring
  ↓
Failure analysis
  ↓
Retraining
```

## Model registry

Every deployable model should record:

- model_id;
- task;
- dataset_version;
- training code commit;
- model checksum;
- hardware;
- latency;
- memory;
- accuracy metrics;
- calibration metrics;
- OOD metrics;
- known limitations;
- dependency/license information;
- approval state;
- deployment history.

## Monitoring

Runtime telemetry should capture:
- inference latency;
- dropped frames;
- sensor health;
- synchronization drift;
- confidence;
- uncertainty;
- OOD score;
- abstention rate;
- human-review rate;
- safety interventions;
- task success/failure.

## Release gates

A model cannot be promoted solely because its accuracy increased.

Promotion requires:
1. regression evaluation;
2. robustness evaluation;
3. calibration evaluation;
4. OOD/abstention evaluation;
5. safety regression;
6. license/supply-chain review;
7. reproducibility record.

## Fleet learning

`Robot → Mission → Data → Failure → Label/Review → Training → Validation → Approved OTA → Robot`

This creates the PUI89 data flywheel while preserving controlled deployment.

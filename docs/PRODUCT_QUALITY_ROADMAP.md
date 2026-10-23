# Product Quality Roadmap — Coconut Harvest AI

**Priority:** Equal top priority across all PUI89 projects.  
**Current evidence level:** software/data-quality prototype; no validated field harvesting system.

## Release gates

1. **Dataset integrity:** verify source, permission/license, image hash, annotation format and geometry, maturity-label definition, and independent human review. Block training/evaluation when any required evidence is missing.
2. **Leakage-safe evaluation:** group related images by tree, source, session, or capture sequence before splitting. Keep a frozen held-out set; test exact and near duplicates where feasible.
3. **Baseline measurement:** record code revision, dataset version, model/checkpoint and license, hardware/software environment, thresholds, IoU definition, per-class precision/recall, mAP where applicable, confusion matrix, latency, and memory. Never substitute example output for a real run.
4. **Safe decision support:** uncertain target, stale/missing sensor, unverified geometry, human in exclusion zone, collision risk, or unhealthy safety channel must prevent cutting. Model output must not directly command actuators.
5. **Hardware validation:** independently test reach, load, stability, grasp/capture, cutting, lowering, emergency stop, watchdog, and power-loss response before any field capability claim.

## Milestones

- [ ] Clear dataset provenance and annotation blockers.
- [ ] Publish a reviewed dataset manifest and frozen split.
- [ ] Run a reproducible local baseline and publish actual metrics and failure examples.
- [ ] Compare compatible baselines on the same test split.
- [ ] Validate safety logic with fault injection; keep hardware validation separate.
- [ ] Publish install/run instructions, model/data/license notes, limitations, and rollback steps.

## Resource policy

Prefer dependency-light tests and local CPU/GPU execution. Do not auto-download large weights, train in routine CI, add paid services, or commit large model files. Check licenses and costs before adopting any model or dataset.

## Honest status rule

The 0–30 m palm-height range is a design goal, not demonstrated reach. CI success establishes only the checks actually run. Do not claim detector accuracy, real harvest success, or physical safety without corresponding evidence.

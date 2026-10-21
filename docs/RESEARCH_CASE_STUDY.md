# Coconut Harvest AI — Research Case Study

**Project type:** Practice-oriented AI application and agricultural-robotics prototype  
**Status:** Software prototype; real-world harvesting capability is not validated  
**Project repository:** https://github.com/Pui89/Coconut-Harvest-AI

## Practical problem

Coconut inspection and harvesting involve partially occluded fruit, variable lighting, uncertain harvest stage, depth and pose uncertainty, obstacles, and the consequences of an unsafe cut or robot movement. A useful system must do more than draw bounding boxes: it should expose uncertainty, assess whether a target is actionable, and defer when evidence or safety conditions are inadequate.

## What is implemented

The repository contains a local-first planning prototype, a synthetic orchard workflow, RGB/depth-related components, harvestability scoring, sensor-health checks, safety-gate logic, annotation and dataset-audit utilities, and reproducible evaluation tools for externally generated detections. Automated regression tests are run through GitHub Actions.

These components demonstrate software structure and testable workflow behaviour. They do **not** establish that a trained detector generalises to real orchards or that a physical robot can safely harvest coconuts.

## Current evidence and limitations

- The documented initial two-image HSV smoke-test baseline has **precision 0 and recall 0 at IoU ≥ 0.50**. It is a failure baseline, not evidence of useful detection accuracy.
- Evaluation and detector-comparison tools can score supplied prediction exports against reviewed ground truth, but they do not themselves run a detector.
- The repository's illustrative orchard photographs are references, not labelled training examples or model predictions.
- Real-orchard generalisation, maturity classification, calibrated 3D targeting, end-to-end arm control, and physical harvesting remain unvalidated.

## Proposed research questions

1. How robustly can a vision system detect and localise coconuts under occlusion, illumination changes, and viewpoint variation?
2. How should detection confidence, depth quality, and target reachability be combined so that the system can abstain rather than produce unsafe actions?
3. Does an uncertainty-aware, safety-gated workflow reduce unsafe or unsupported target selections compared with a detector-only or fixed-threshold baseline?

## Reproducible evaluation plan

1. **Data governance:** record each image's source, licence/permission, capture conditions, and group identity. Exclude images without clear reuse rights.
2. **Annotation and quality assurance:** annotate visible fruit with a documented box convention; review ambiguous and occluded instances; record inter-review disagreements where feasible.
3. **Leakage-resistant split:** separate train/validation/test data by source image or orchard/session where metadata permits; audit exact duplicates and source groups before evaluation.
4. **Detector baseline:** run a compatible, locally available model on the frozen test set and save raw predictions, model/version/configuration, confidence threshold, and hardware/software environment.
5. **Metrics:** report precision, recall, F1, and average precision where the evaluation protocol supports it; state IoU thresholds, class definitions, sample counts, and confidence-threshold selection. Report latency separately from accuracy.
6. **Robustness and abstention:** stratify results by occlusion and lighting; test missing or invalid depth, low confidence, and unreachable targets; report false actions, abstentions, and safety-gate outcomes.
7. **Reproducibility:** publish commands, data-manifest schema, configuration, per-image predictions, aggregate metrics, and known limitations without redistributing images unless permitted.

No future metric is claimed here. Results should be added only after the corresponding experiment has actually run.

## Safety and deployment boundary

The current project is a research/software prototype. Any future physical trial would require supervised operation, emergency stop, exclusion zones, verified robot kinematics and tool geometry, and a staged risk assessment. A software test passing is not proof of physical safety.

## Why this is a practice-oriented AI case study

The project connects a real agricultural workflow to applied perception, uncertainty handling, decision-making, verification, and human oversight. It provides a concrete basis for investigating how AI components can be evaluated as part of a larger system, including how failures are surfaced and how claims are bounded by evidence.

## Next milestone

Complete a rights-cleared, human-reviewed real-image benchmark and publish the first reproducible detector results. Start with [the real-image benchmark checklist](FIRST_REAL_IMAGE_BENCHMARK_CHECKLIST.md) and the [product benchmark standard](PRODUCT_BENCHMARK_STANDARD.md).

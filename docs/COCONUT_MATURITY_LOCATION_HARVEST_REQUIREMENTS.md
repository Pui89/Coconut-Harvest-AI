# Coconut Detection, Maturity, 3D Location, and Harvest Eligibility

**Status:** design requirements; not a validated detector or physical harvesting system.

## Purpose

Specify an evidence-driven AI pipeline that detects individual coconuts, assigns a maturity class, estimates fruit location with uncertainty, and requests a harvest only when independent safety conditions are satisfied. The intended orchard design envelope includes trees from 0 to 30 metres tall. **This is a design target, not evidence that a robot arm can reach or harvest at 30 m.**

## 1. Detection and maturity labels

Use separate, explicit labels:

- `young_green` — young green fruit; normally do not select for harvest unless the product objective explicitly requests it.
- `mature_green` — mature green fruit; a potential harvest candidate only after maturity, reach, safety, and collection checks pass.
- `brown_aging` — brown/aging fruit; do not infer readiness from colour alone. Product-specific criteria are required.
- `uncertain` — insufficient visual evidence, occlusion, conflicting sensors, or low confidence. This class must never authorize cutting.

The taxonomy and boundaries must be reviewed by a qualified agricultural/domain reviewer. Colour alone is not ground truth for physiological maturity. Record ambiguous cases instead of forcing a label.

## 2. Per-fruit output record

For every detected fruit, preserve a machine-readable record with:

| Field | Meaning |
|---|---|
| `fruit_id` | Stable ID within the current image/scene; do not imply identity across sessions without tracking evidence |
| `bbox_xyxy` or `mask` | Image-space box or segmentation, with image dimensions recorded |
| `maturity_class` | One of the four labels above |
| `class_confidence` | Model score with documented meaning; not automatically a calibrated probability |
| `image_id` | Source image/scene ID and provenance record |
| `position_3d_m` | Optional x/y/z estimate in a declared coordinate frame, only when calibration and suitable depth/geometry exist |
| `position_uncertainty` | Error/uncertainty representation and method; never silently replace unknown with zero |
| `tree_height_m` | Optional estimated height with method and uncertainty; distinguish measured, inferred, and unknown |
| `reachability` | `reachable`, `unreachable`, or `unknown`, based on a verified robot workspace model |
| `capture_ready` | `true`, `false`, or `unknown` |
| `safety_decision` | `stop`, `review_required`, or `eligible_for_supervised_authorization` |
| `reason_codes` | Explicit reasons for rejection/hold, such as `sensor_fault`, `uncertain_maturity`, `outside_verified_workspace`, `obstacle`, `capture_not_ready` |
| `timestamp` | Timestamp with timezone or monotonic run-time convention documented |

Image-space location is not 3D position. A monocular image alone does not establish absolute distance or tree height without suitable calibration, known scale, or additional sensing. RGB-D/LiDAR data must be calibrated and checked for validity, alignment, range and dropout before use.

## 3. Processing pipeline

1. Validate image/sensor inputs, timestamps, calibration, and sensor health.
2. Detect individual fruits; preserve boxes/masks and model version.
3. Classify maturity into the defined taxonomy, including an uncertainty path.
4. Estimate 3D fruit location only if calibrated depth/geometry is valid; propagate uncertainty.
5. Estimate tree height separately and record its source/method.
6. Check the target against a verified robot workspace and current configuration. Do not extrapolate workspace to 30 m without mechanical evidence.
7. Check obstacles, overhead electrical lines, people, wind/environmental limits defined by engineering review, base stability, localization, arm state, and collection readiness.
8. Produce a logged decision. Any missing, stale, contradictory, non-finite, out-of-range, or uncertain safety input means stop/hold; never default to safe.
9. Only a separately validated safety controller and required human supervision may authorize physical actuation. This document does not define a direct actuator command interface.

## 4. Harvest eligibility policy

A fruit may be marked `eligible_for_supervised_authorization` only if all required conditions are positively verified:

- The maturity class is allowed by the selected harvest objective.
- Detection and location quality satisfy thresholds established from a representative validation study.
- The location lies within a mechanically verified workspace with adequate margin for uncertainty.
- Required localization, camera/depth sensors, calibration and communications are healthy and current.
- The path and work zone are clear; people and other hazards are outside defined exclusion zones.
- The robot base and arm are stable within independently established operating limits.
- The capture/collection mechanism is ready to control the fruit and prevent an uncontrolled fall.
- An independent safety controller/interlock reports safe state and required supervision is present.

Otherwise return `stop` or `review_required`, with reason codes. Do not invent confidence thresholds, wind limits, reach accuracy, payload limits, or stability limits; set them only through risk assessment and measured validation. Human approval alone does not replace interlocks.

## 5. Evaluation plan and required statistics

Report measured results by maturity class and relevant conditions, not just one aggregate score:

- Dataset: image/scene count, fruit-instance count, source/licence, annotation protocol, reviewer/QA status, and train/validation/test split.
- Leakage control: split by tree/source/session where possible; near-duplicate images must not cross splits.
- Detection: precision, recall, F1, and IoU/mAP as appropriate to the annotation format; publish the matching rule and thresholds.
- Maturity: per-class precision/recall/F1, confusion matrix, and macro-F1; separately report uncertain/abstained predictions.
- Localization: position error and uncertainty calibration only where trustworthy 3D ground truth exists.
- Robustness: stratify by lighting, occlusion, camera distance/viewpoint, bunch density and maturity class when the dataset supports it.
- Runtime: device, model/runtime versions, image dimensions, warm-up, number of repetitions, median and tail latency, memory use, and failures.
- Safety decision: test-case denominator, false-allow count, stop/hold behavior under missing and faulty inputs, and evidence of independent interlock testing.
- End-to-end task completion, fruit damage, and physical cut/capture success must be reported only after controlled, appropriately safe tests; simulation results must be labelled separately.

No performance number should be reported until a reproducible run has actually been completed. Synthetic fixtures are useful for software tests but are not evidence of real-world accuracy. Keep a held-out evaluation set untouched during tuning.

## 6. Minimum regression and fault-injection tests

- Each of the four maturity labels maps to the documented policy.
- Low/ambiguous maturity confidence never enables cutting.
- Missing or invalid depth, calibration mismatch, stale timestamp, NaN/Inf coordinate, or out-of-range position produces stop/hold.
- Fruit outside the verified workspace or with excessive position uncertainty cannot be selected.
- Obstacle, person in exclusion zone, unstable base, wind-limit input unknown, or capture-system fault prevents cutting.
- Model crash, camera failure, network loss, and watchdog/interlock fault disable hazardous actuation through the independent safety architecture.
- Empty images, malformed records, wrong image dimensions, duplicate IDs and unsupported labels are rejected clearly.
- Logs include the decision and reason codes without exposing secrets or unnecessary personal data.

## 7. 0–30 m concept boundary

The 0–30 m value describes the intended tree-height design envelope only. Before any physical operation at a given height, the engineering team must demonstrate a suitable reach mechanism, structural stability, load/payload and deflection limits, sensing accuracy, collision clearance, controlled fruit capture, emergency stop/holding behavior, and staged test evidence. Tall-tree work introduces significant falling-object, overhead-line, wind, and tip-over hazards. If the mechanism or safe exclusion zone is not validated for a target, the correct output is `unreachable` or `unknown`, not a cut command.

## 8. Evidence checklist

- [ ] Maturity taxonomy and annotation guide reviewed by a domain expert.
- [ ] Source permissions/licences and provenance verified for each evaluation image.
- [ ] Human-reviewed labels and independent QA recorded.
- [ ] Leakage-safe train/validation/held-out test split frozen.
- [ ] Baseline and model versions, command, environment, and results recorded.
- [ ] Per-class metrics and confusion matrix published with sample counts.
- [ ] 3D calibration and localization ground truth validated before reporting metric values.
- [ ] Fault-injection and fail-closed tests pass in the actual test run.
- [ ] Simulation, bench tests, and physical field trials are reported separately.
- [ ] Mechanical workspace and safe cutting/capture capability are independently verified before actuation claims.

## Current implementation status

This file specifies requirements and evaluation criteria only. It does not claim that a detector, maturity classifier, calibrated 3D locator, 30 m arm, or physical cutting system has been implemented or validated. Record implementation and results separately after inspecting code and running tests.

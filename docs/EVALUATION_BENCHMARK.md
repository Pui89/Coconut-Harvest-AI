# Evaluation Benchmark

Measure before claiming autonomy.

| Area | Metrics |
|---|---|
| Detection | precision, recall, F1, mAP50, mAP50-95 |
| Segmentation | IoU, boundary quality |
| Tracking | IDF1, HOTA, track stability |
| 3D | depth MAE, 3D localization error |
| Harvestability | calibration, abstention rate, false-harvest rate |
| Planning | success rate, path length, planning time |
| Robotics | harvest success, failed harvest, collision rate, cycle time, energy/tree |
| Safety | unsafe-action rate, E-stop response, human-detection failure, sensor-failure recovery |
| Operations | uptime, battery consumption, maintenance time, cost/tree |

Evaluate across lighting, weather, canopy density, distance, occlusion, tree height, sensor configuration and hardware profile. Record dataset/model provenance and confidence intervals where possible.

## Minimum reproducible experiment record

Copy this checklist into every experiment report. Use `NOT RUN` or `NOT MEASURED` rather than leaving a blank field or estimating a result.

- **Experiment ID / date:**
- **Question being tested:**
- **Code commit:**
- **Dataset version and manifest SHA-256:**
- **Source/licence review status:**
- **Split policy:** group by source, orchard/tree, capture session, or near-duplicate family to prevent leakage.
- **Train / validation / test image counts:** report image and scene counts separately.
- **Model and checkpoint:** include exact model name/version and checkpoint SHA-256; write `NONE — heuristic baseline` when applicable.
- **Environment:** OS, Python, package versions, CPU/GPU model, and inference settings.
- **Decision threshold / confidence policy:**
- **Metrics and units:** include the IoU threshold for box metrics and latency hardware/batch size.
- **Per-class results:** report every evaluated class, including classes with zero examples or zero detections.
- **Failure review:** false positives, missed visible fruit, merged/split fruit, occlusion, blur, lighting, and uncertain maturity.
- **Limitations and next action:**

## Coconut-specific evaluation rules

1. Keep **detection** and **maturity classification** separate. A correct box does not prove the maturity label is correct.
2. Report young green, mature green, mature brown/dry, mixed-stage bunch, and uncertain/occluded cases separately only when the labels have agreed operational definitions and sufficient reviewed examples. Do not silently merge uncertain fruit into a confident class.
3. Use a frozen, held-out test set only once for final comparisons. Use validation data for threshold/model selection; document any test-set reuse.
4. Report counts alongside percentages. With a tiny test set, one mistake can change a metric substantially; state that uncertainty plainly.
5. For a rule-based or colour heuristic, call it a **heuristic baseline**, not a trained AI model. For a model that was not actually run, report no score.
6. Report inference latency separately from image capture, sensor processing, robot motion, cutting, collection, and total cycle time.
7. Perception metrics do not establish safe reachability, successful cutting, fruit retention, safe lowering, or successful harvest. Those require separate, supervised validation and outcome evidence.
8. Do not publish images, derived crops, overlays, or dataset copies until the relevant source licence/permission and attribution requirements are checked.


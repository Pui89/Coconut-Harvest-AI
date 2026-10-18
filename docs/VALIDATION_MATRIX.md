# Validation Matrix — Coconut Harvest AI

Last reviewed: 18 October 2026. Status is evidence-based; a code file existing does not mean the capability has been validated.

| Capability | Repository evidence | Current status | What is still required |
|---|---|---|---|
| Local application and workflow orchestration | `apps/pui89_app/`, `demo_end_to_end.py` | Prototype code and tests exist | Confirm current full CI run passes; inspect generated audit reports |
| Detection adapter and IoU tracking baseline | `local_detector.py`, `iou_tracker.py` | Integration interfaces/baseline exist | Independent labelled orchard test set; precision, recall, mAP, latency and failure examples |
| RGB-D localisation | `rgbd_localization.py` | Localisation interface exists | Camera/depth calibration and error measured against reference positions |
| Harvest-target eligibility and safety gate | `robot_workflow.py`, `src/coconut_harvest_robot/safety_gate.py` | Software preflight checks exist; malformed numeric inputs now fail closed | Current CI run must pass; hardware-specific risk analysis and independent safety review |
| Dataset intake and annotation | `training/`, `tools/`, `scripts/prepare_real_image_review.py` | Local workflow tools exist | Actual images collected, rights reviewed, boxes human-verified, group leakage audit passed |
| Training and test evaluation | `training/train_detector.py`, `training/evaluate_detector.py` | Reproducible local scripts exist; no trained result asserted here | Licensed local checkpoint + complete dataset; train and evaluate on frozen held-out test set |
| Simulation | Simulated workflow and demo tests | Software simulation path exists | Full robot model, sensor simulation, collision and recovery scenarios with recorded evidence |
| Physical harvesting | No evidence of completed hardware harvest in this repository status | **Not validated** | Robot arm, cutter, interlocks, calibration, supervised dry runs, safety review and measured trials |

## Latest safety hardening

The software gate blocks emergency-stop state, human exclusion-zone occupancy, failed collision checks, low/invalid confidence, invalid or negative motion/force/height values, non-finite values, and invalid configured safety limits. It is defence-in-depth software only, not a certified safety controller.

## Rules for publishing results

- Never call a candidate image a labelled training sample until the label has been reviewed.
- Never use training or validation images to claim held-out test performance.
- Record dataset/checkpoint hashes, exact configuration, environment, failure cases and the CI run URL.
- Mark unexecuted tests **NOT RUN**. Do not infer physical safety or harvest success from simulation alone.

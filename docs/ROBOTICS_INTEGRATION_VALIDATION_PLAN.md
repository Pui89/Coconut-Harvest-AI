# Coconut Harvest AI — Robotics Integration and Validation Plan

**Status:** planning document. The presence of a planned interface does not mean the corresponding robot, sensor, or control loop has been implemented or tested.

## Objective

Define a staged, simulation-first path from image-based coconut perception to a safely constrained harvesting-robot demonstration. The first deliverable is a reproducible software pipeline; physical cutting is explicitly out of scope until separate safety and field validation gates are met.

## Proposed system pipeline

1. **Image input** — use a versioned, rights-reviewed dataset or a documented camera stream. Preserve timestamps and camera calibration when available.
2. **Perception** — run a detector that has been evaluated on a frozen, human-annotated test split. Report precision, recall, F1 and the chosen confidence/IoU thresholds. Record false positives and missed coconuts.
3. **Tracking** — associate detections across frames only when a video sequence and suitable evaluation labels exist. Report tracking metrics separately; image detection scores are not tracking scores.
4. **3D localisation** — estimate a target position only when calibrated depth, stereo, or another justified geometric source is available. Record coordinate frame, units, calibration and uncertainty. A 2D bounding box alone is not a 3D position.
5. **Planning interface** — pass a target candidate to a simulator or planning module with explicit validity checks, workspace limits and a reject/stop path. Do not send perception output directly to a physical actuator.
6. **Simulation** — test target selection, reachable/unreachable targets, occlusion, stale observations, sensor dropouts and emergency-stop behaviour before considering hardware.
7. **Human-reviewed report** — save the software commit, model/checkpoint identity, dataset split, configuration, command, outputs and failure cases for each experiment.

## Implementation status ledger

Update this table only when evidence exists in the repository.

| Capability | Evidence required before calling it implemented |
|---|---|
| Coconut detection | Compatible model and weights, runnable inference command, saved predictions and evaluation on reviewed held-out images |
| Video tracking | Sequence-level test data, identity annotations, reproducible tracker run and tracking-specific metrics |
| 3D target localisation | Sensor/calibration details, coordinate-frame tests, error measurements against reference positions |
| Motion planning | Executable planner or simulator configuration, documented constraints, successful and failed test cases |
| Robot simulation | Reproducible launch instructions, model/world assets and recorded test results |
| Physical harvesting | Separate risk assessment, guarded test setup, emergency stop and interlocks, qualified supervision, and staged validation evidence |

Until evidence is added, describe these capabilities as **planned**, **in development**, or **not yet validated** as appropriate. A concept image is illustrative, not evidence that a robot or function exists.

## Minimum simulation test matrix

- Valid target with clear visibility.
- Multiple candidate targets and deterministic target selection.
- Partially occluded target and low-confidence detection.
- No detection, invalid coordinates, NaN values, or stale timestamps.
- Target outside the permitted workspace.
- Unreachable target or planner failure.
- Missing or inconsistent depth/calibration.
- Sensor message loss and delayed messages.
- Stop request during every simulated stage.
- Restart after a fault without automatically resuming motion.

For each case, record the input, expected response, actual response, pass/fail, software commit and relevant logs. The safe default for invalid or uncertain inputs is to reject the target and keep actuation disabled.

## Research questions worth testing

1. How do lighting, occlusion and viewing angle affect coconut detection errors on a fixed held-out set?
2. Does tracking reduce duplicate target selections in video, and what new failure modes does it introduce?
3. How does depth availability and calibration error affect target-position error?
4. Which failure cases should trigger abstention rather than a motion-planning request?

Choose one primary question for the first study. Define the dataset, baseline, metrics and success criterion before examining test-set results.

## Safety boundary

This plan is not a safety certification. Keep physical actuators disabled during initial work. No cutting or robot movement should be triggered solely by a detector output. Any future hardware trial requires a separate documented risk assessment, guarding, emergency stop, independent interlocks, qualified supervision and staged validation.
# Complete System Blueprint — Coconut Harvest AI

**Scope:** local-first AI application plus simulation-first agricultural robot. This is an implementation blueprint and acceptance checklist, not a claim that physical harvesting is complete.

## System architecture

```text
RGB / depth / LiDAR / robot state
  -> timestamp, calibration and sensor-health checks
  -> coconut perception adapter (model + confidence + version)
  -> 2D tracking and 3D target localisation
  -> target eligibility gate (visibility, depth validity, uncertainty, exclusion zones)
  -> reachability and collision-aware motion-planning interface
  -> simulation-only task executor
  -> human approval / emergency-stop / fault state
  -> append-only JSON event and experiment report
```

## Component contracts

1. **Sensors:** every observation carries timestamp, frame ID, calibration version and source. Missing/stale/un-calibrated depth must not be replaced with invented coordinates.
2. **Perception:** return class, confidence, bounding box/mask, model/checkpoint identifier and input identifier. Keep unknown/ambiguous detections.
3. **Tracking:** associate observations across frames; report track age and uncertainty. Tracking is not proof of a correct detection.
4. **3D localisation:** use calibrated depth or point cloud; reject invalid depth and points outside configured working range. Record localisation error against measured ground truth before making accuracy claims.
5. **Task planner:** return a proposed target and trajectory only. Check reachability, joint limits, collision geometry, target stability and human exclusion zones.
6. **Safety supervisor:** default to STOP on missing data, stale observations, uncertain target, sensor disagreement, collision, communication loss or emergency stop. No autonomous cutting until a separate, reviewed safety case and hardware tests exist.
7. **Audit:** record inputs, model/config versions, decision reason, safety state and outcome without storing unnecessary personal data.

## Free-first development profile

- Use local Python tools and public, licence-reviewed data; no paid inference API or cloud GPU is required.
- ROS 2 + Gazebo can be introduced on a compatible Linux environment. The official Nav2 setup path covers robot description, transforms, odometry, sensors, mapping, footprint, planners and controllers: https://docs.nav2.org/jazzy/configuration_and_development/first_time_robot_setup_guide/gazebo/
- Keep downloaded images, labels and model weights out of Git unless their licence explicitly permits redistribution.
- Pin dependency versions and record the operating system, Python version, model hash and dataset version for every experiment.

## Acceptance gates

- [ ] Unit tests cover malformed inputs, stale frames, invalid depth, confidence thresholds and unknown classes.
- [ ] Dataset manifest passes licence/provenance audit; human-verified labels and independent split groups are recorded.
- [ ] Training and evaluation use separate train/validation/test groups; report precision, recall, mAP (where applicable), latency, failures and confidence threshold.
- [ ] RGB-D localisation error is measured against independent reference points.
- [ ] Simulation tests cover unreachable targets, collision, joint-limit violations, sensor loss, emergency stop and restart recovery.
- [ ] Hardware tests begin with motors/cutter disabled, supervised dry runs and documented risk assessment.
- [ ] Any field or harvesting claim cites a dated protocol, hardware configuration, sample size and measured result.

## Current boundary

The repository already contains a software prototype and data-preparation tools. This document does not establish that a trained detector, calibrated RGB-D localisation, validated arm planner or physical harvesting system has passed these gates. Report each gate as **PASS**, **FAIL**, or **NOT RUN** with evidence.
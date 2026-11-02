# AI Development Roadmap

## Phase 1 — Perception
- Replace the placeholder detector with a YOLO training/inference adapter.
- Add coconut, cluster, trunk, branch, person, animal and obstacle labels.
- Add SAM 3 segmentation/tracking adapter.
- Build a coconut ripeness benchmark.

## Phase 2 — 3D world model
- RGB-D calibration and point-cloud fusion.
- LiDAR integration.
- Tree/canopy semantic map.
- 3D coconut localization and reachability scoring.

## Phase 3 — Vision-language reasoning
- Add Gemma 4 31B IT adapter.
- Convert natural-language harvest requests into structured goals.
- Add scene-questioning and uncertainty reporting.

## Phase 4 — Action policies
- Add LeRobot-compatible datasets.
- Evaluate SmolVLA/OpenVLA/GR00T/pi0-family policies.
- Train from demonstrations in simulation.
- Keep motor control behind the safety layer.

## Phase 5 — Planning and ROS 2
- Integrate MoveIt 2 and OMPL.
- Add RRT* / collision-aware planning.
- Integrate Nav2 for mobile-base navigation.
- Add deterministic execution state machines.

## Phase 6 — Anomaly and recovery
- Sensor-health monitoring.
- Environmental anomaly detection.
- AI uncertainty detection.
- Stop/retract/replan/recover behaviors.

## Phase 7 — Digital twin
- Build the orchard in Isaac Sim/Isaac Lab.
- Generate synthetic RGB/depth/segmentation data.
- Domain randomization.
- Hardware-in-the-loop testing.

## Phase 8 — Real robot
- Calibrate sensors and robot.
- Low-speed dry runs.
- Empty-tool tests.
- Controlled harvesting trials.
- Expand operating envelope only after safety validation.

# Reproducible Orchard Benchmarks and Next-Stage Build Plan

Status: evaluation tooling and protocol; not evidence of production readiness.

## Main engineering gap

The repository describes detection, ripeness scoring, 3D localization, arm planning and execution. The critical missing proof is a reproducible chain from a real or recorded orchard scene to a safe, completed harvest, with failures counted. Random tensors or a visually convincing concept do not establish field performance.

## Added benchmark metadata gate

`tools/validate_benchmark_report.py` uses only the Python standard library. It rejects missing provenance, placeholder text, timestamps without a timezone, and non-numeric/non-finite metric values.

```bash
python tools/validate_benchmark_report.py benchmarks/reports/orchard-run.json
pytest -q tests/test_benchmark_report_validator.py
```

This checks report structure only, not the truth of results or physical safety. Never invent metrics. Preserve the dataset version, model checkpoint hash, Git commit, hardware, calibration and configuration for each run.

## Minimum evaluation matrix

| Test slice | Metrics to publish |
|---|---|
| Ripe/unripe/occluded coconuts | per-class precision, recall, F1, confusion matrix |
| Different cultivars, seasons and sunlight | performance by condition; held-out orchard generalization |
| Depth holes, reflective leaves, sensor misalignment | 3D localization error and failure/abstention rate |
| Multiple fruits and overlapping canopy | duplicate/missed detections; target-selection accuracy |
| Arm reachability | reachable-target rate and false-reachable rate |
| Trajectory planning | planning success, collision count, minimum clearance, plan time |
| Picking trials | successful pick rate, fruit damage, missed cuts, dropped fruit |
| Recovery / fault injection | safe-stop latency, watchdog response, recovery success |
| Edge deployment | p50/p95 inference and cycle latency, FPS, RAM/VRAM, power |
| Repeated full missions | completed trees/hour, human interventions, downtime |

Report sample counts and uncertainty intervals; keep train/validation/test scenes separated by tree, orchard or collection session to avoid leakage. Publish failed attempts, not only successful demonstrations.

## Open-source stack to evaluate

Check exact version, model-weight and dependency licenses before commercial use. A library's license does not automatically cover its weights or data.

- ROS 2 (Apache-2.0): https://github.com/ros2/ros2 — sensor drivers, lifecycle nodes and robot integration.
- MoveIt 2 (BSD-3-Clause): https://github.com/moveit/moveit2 — manipulation planning and collision checking.
- Gazebo Sim (Apache-2.0): https://github.com/gazebosim/gz-sim — robot, sensor and orchard simulation.
- Open3D (MIT): https://github.com/isl-org/Open3D — point clouds, registration and 3D geometry.
- OpenCV (Apache-2.0): https://github.com/opencv/opencv — image processing and camera pipelines.
- FiftyOne (Apache-2.0): https://github.com/voxel51/fiftyone — dataset review, error slices and annotation QA.
- CVAT (MIT): https://github.com/cvat-ai/cvat — image/video annotation workflow.
- DVC (Apache-2.0): https://github.com/iterative/dvc — dataset and experiment versioning.
- MLflow (Apache-2.0): https://github.com/mlflow/mlflow — experiment tracking and artifacts.
- OpenSSF Scorecard (Apache-2.0): https://github.com/ossf/scorecard — dependency and repository supply-chain checks.

If using Ultralytics YOLO, explicitly review its AGPL-3.0 and enterprise licensing options before shipping a closed commercial product. Do not assume every checkpoint or dataset has the same terms.

## Safety and release gates

1. Test planning in simulation before commanding physical actuators.
2. Enforce joint limits, velocity/force limits, tool interlocks, collision checking and an independently tested emergency stop.
3. A target with uncertain depth, occluded stem, unstable branch or unsafe reach must be rejected or sent to human review.
4. Fault injection must cover camera disconnect, stale transforms, actuator timeout, unexpected load and communications loss.
5. Begin with an instrumented, low-energy mock setup; do not place people under test loads or near an unvalidated cutting tool.
6. Do not call the system autonomous or production-ready until repeated full-mission trials on the target hardware support that claim.

## Next implementation sequence

1. Freeze a labelled orchard dataset and publish annotation and split policies.
2. Add camera calibration, RGB-depth alignment checks and uncertainty-aware 3D target estimates.
3. Implement ROS 2 sensor/arm interfaces with health monitoring and explicit safe states.
4. Build a Gazebo/MoveIt simulation of reachability, branch obstacles, cut/grasp, retraction and drop placement.
5. Run repeatable end-to-end tests and publish benchmark JSON plus failure videos/logs.
6. Test on hardware using a mock fruit/branch fixture before controlled orchard trials.

## Required report fields

Include `schema_version`, `project`, `run_id`, timezone-aware `run_date_utc`, `dataset{name,version,split}`, `model{name,version}`, `hardware{platform}`, `software{os,python}`, `config{seed}` and numeric `metrics`. Include metric definitions and trial counts in the report narrative.

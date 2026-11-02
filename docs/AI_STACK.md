# Embodied AI Stack

This document defines the open-source AI architecture for the Coconut Harvest Robot.

## Core loop

SEE -> UNDERSTAND -> LOCATE -> PREDICT -> PLAN -> SAFETY CHECK -> ACT -> VERIFY -> LEARN

## Model roles

| Layer | Recommended open-source component | Role |
|---|---|---|
| Fast detection | YOLO family | Real-time coconut, person, animal and obstacle detection |
| Segmentation | SAM 3 | Instance/semantic segmentation and video tracking |
| Vision reasoning | Gemma 4 31B IT | Image/video understanding, spatial reasoning and task interpretation |
| 3D geometry | Open3D + RGB-D/LiDAR | Point clouds, 3D localization and semantic maps |
| VLA / action | NVIDIA GR00T, SmolVLA, OpenVLA, pi0 family | Convert observations and task intent into robot actions |
| Navigation | ROS 2 Nav2 / ROS 2 Nav2 | Base navigation and waypoint-level reasoning |
| Manipulation | MoveIt 2 + OMPL/RRT* | IK, collision checking and motion planning |
| Simulation | Isaac Sim + Isaac Lab | Digital twin, synthetic data, domain randomization and sim-to-real |
| Deployment | PyTorch + Transformers + ONNX/TensorRT/vLLM | Training and efficient inference |

## Safety boundary

Large vision and action models are NOT connected directly to motor drivers.

Every proposed action must pass:

1. Workspace and joint-limit validation.
2. Collision checking.
3. Human/animal exclusion-zone checks.
4. Velocity, acceleration and force limits.
5. Model confidence / uncertainty checks.
6. Emergency-stop state.
7. Post-action verification.

## Coconut-specific perception

Recommended classes:

- coconut
- ripe_coconut
- unripe_coconut
- coconut_cluster
- trunk
- branch
- leaf
- person
- animal
- obstacle
- robot

The ripeness subsystem should combine visual appearance with temporal observations and, where available, multispectral/depth information.

## Abnormal-event detection

### Environment
- unexpected human or animal
- falling fruit
- unstable branch
- severe occlusion
- poor visibility
- unexpected obstacle

### Robot
- motor overload
- collision/contact
- wheel slip
- camera/depth failure
- overheating
- low battery
- communication loss

### AI
- low detector confidence
- unknown object
- inconsistent depth
- segmentation failure
- planner/VLA disagreement
- action uncertainty

Severity levels: NORMAL -> SUSPICIOUS -> WARNING -> CRITICAL -> EMERGENCY

## Data and training

Use simulation-first development where practical:

1. Build the orchard digital twin.
2. Generate RGB, depth, segmentation and pose data.
3. Train/fine-tune perception models.
4. Apply domain randomization.
5. Train/evaluate action policies from demonstrations.
6. Validate safety constraints.
7. Run hardware-in-the-loop.
8. Transfer to the real robot.

Do not commit model weights or private datasets to this repository. Store dataset manifests and download instructions instead.

## ROS 2 integration

Suggested node boundaries:
- camera_node
- lidar_node
- yolo_detector
- sam_segmenter
- gemma_vlm
- world_model
- ripeness_estimator
- anomaly_detector
- task_planner
- vla_policy
- safety_validator
- moveit_controller
- harvest_verifier

This separation keeps experimental AI models replaceable while maintaining a deterministic robotics and safety layer.

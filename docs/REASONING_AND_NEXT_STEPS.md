# Reasoning Layer and Next Steps

The coconut robot now has a high-level reasoning adapter designed for Gemma 4 31B IT or another vision-language reasoning model.

## Layered architecture

Perception (YOLO/SAM3/depth) -> 3D scene/world state -> reasoning model -> task planner/VLA -> deterministic safety gate -> robot controller.

The reasoning model proposes goals and explanations. It never sends motor commands directly.

## What to add next

1. **World model** — persistent 3D map of trees, branches, targets, robot pose and free space.
2. **Active perception** — deliberately move the camera/robot when a target is occluded or uncertain.
3. **Skill library** — reusable skills such as approach, inspect, grasp, cut, retract and verify.
4. **Force/torque sensing** — detect branch contact, tool jams and unexpected load.
5. **Target memory** — remember inspected/harvested/failed targets across a tree.
6. **Uncertainty calibration** — measure confidence against real harvest outcomes instead of trusting raw model scores.
7. **Simulation and digital twin** — Isaac Sim/Isaac Lab scenes with wind, leaves, occlusion, lighting and tool contact.
8. **LeRobot datasets** — record demonstrations, failed attempts and recovery actions as structured episodes.
9. **Evaluation suite** — target-selection accuracy, collision rate, harvest success, false cuts, time-to-harvest and recovery rate.
10. **Human override** — explicit remote approval for low-confidence or safety-critical actions.

## Key principle

Reasoning decides *what should happen*; the planner decides *how to execute it*; the safety controller decides *whether execution is allowed*.

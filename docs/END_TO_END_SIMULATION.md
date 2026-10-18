# End-to-End Coconut Harvest Simulation Workflow

## Status

This is a software-only research prototype. It runs a synthetic RGB/depth scene through sensor-health checks, the existing neural feature pipeline, harvestability scoring, and a deterministic safety gate. It emits a JSON report and does not issue ROS 2, motor, gripper, or cutter commands.

## Run locally

Install the project and development extras in a virtual environment:

~~~bash
python -m pip install -e ".[dev]"
python demo_end_to_end.py
python -m pytest
~~~

The demo uses generated synthetic imagery. Its evidence values are test fixtures, not predictions measured from the image and not proof that a coconut is ripe, reachable, or safe to harvest.

## Pipeline

1. Sensor health: missing, degraded, or unsynchronized sensors cause a safe hold.
2. Perception proposal: RGB and depth tensors pass through the repository's current neural feature pipeline.
3. Harvestability: explicitly supplied evidence is scored for confidence, localization, ripeness, reachability, clearance, sensor quality, occlusion, and tracking stability.
4. Safety validation: confidence, clearance, speed, force, workspace height, human exclusion, emergency stop, and collision status are checked.
5. Evidence report: JSON records status, reasons, perception tensor summary, and prototype trajectory waypoint count.
6. No actuation: actuator_commands_sent is always false.

## Critical limitations

- The perception network is not a validated coconut detector and the demo does not infer supplied harvestability evidence from image pixels.
- The current trajectory planner has simplified collision logic; its waypoints are not accepted as collision-free.
- The kinematics implementation is a placeholder and is not a validated inverse-kinematics solver.
- The optional YOLO26 adapter is not automatically called by this demo. Its pretrained classes and performance must be checked on a representative orchard dataset.
- No ROS 2 controller, calibrated depth sensor, physical gripper, cutter, or emergency-stop hardware is connected.
- Do not use the output to control a physical robot or to cut/grasp anything.

## Next acceptance gates

1. Add a genuine obstacle-map collision checker and tests for blocked paths.
2. Replace placeholder kinematics with a validated robot-description-based solver and joint-limit checks.
3. Integrate calibrated RGB-D data and target annotations; report precision/recall and 3D localization error on held-out orchard data.
4. Add physics-backed simulation using a validated URDF in Gazebo Sim or Isaac Sim.
5. Conduct hazard analysis, human-exclusion testing, emergency-stop verification, and independent safety review before any physical test.

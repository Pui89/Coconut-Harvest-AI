# Coconut Harvest Robot — concept brief

**Project:** Pui89 Coconut Harvest Robot  
**Design status:** early-stage concept visualization; not a validated or deployment-ready harvesting machine.

## Mission
Develop a low-speed, tracked orchard robot that assists with coconut bunch detection, inspection, reach planning, and supervised harvesting trials. Start in simulation and with mock targets before any live-tree tests.

## Proposed platform
- **Mobility:** compact tracked chassis concept for uneven orchard paths; ground pressure, slope limits, and stability must be measured.
- **Perception:** RGB/stereo or RGB-D camera, optional lidar, lighting-aware detection, and depth estimation.
- **Manipulation:** guarded, low-speed articulated arm with a task-specific end effector. Cutting/gripping geometry and load limits remain to be engineered.
- **Collection:** removable harvest basket; payload and centre-of-gravity limits to be established by testing.
- **Control:** teleoperation-first, emergency stop, speed/force limits, operator confirmation, and a defined exclusion zone.
- **Software:** ROS 2, Gazebo simulation, OpenCV, and MoveIt 2 are candidate open-source components, subject to platform compatibility and license review.

## Development sequence
1. Build a digital mock-up and define tree, fruit-bunch, ground, and obstacle models.
2. Test perception and depth estimates on recorded or synthetic scenes; report precision/recall and localization error with dataset and test conditions.
3. Simulate base navigation, arm reach, collision avoidance, and recovery from failed detections.
4. Use a non-cutting mock end effector and artificial bunches for benchtop manipulation.
5. Conduct supervised field trials only after a documented hazard analysis, emergency-stop test, stability test, and operator training.

## Safety boundaries
- No person under a target bunch or inside the manipulator's exclusion zone.
- Do not perform overhead cutting or live harvesting until mechanical retention, falling-object risk, and safe failure modes are verified.
- Stop on uncertain perception, excessive force, unstable terrain, communication loss, or unexpected people/animals.
- Keep a human operator in control during early testing.

## Evidence and benchmarks
Do not claim autonomous harvesting success until tested. Record detection precision/recall, 3D localization error, reach success rate on mock targets, cycle time, dropped-object rate, emergency-stop response, battery endurance, and terrain conditions. Publish raw results, failures, software versions, and test setup.

## Visual asset
The accompanying [robot concept SVG](./robot-concept.svg) is an illustrative design study. Dimensions, performance, and field capability are not established.

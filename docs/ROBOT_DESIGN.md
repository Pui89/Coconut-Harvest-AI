# Generated Coconut Harvester Robot

This branch adds a concrete simulation/prototyping robot model for the coconut-harvest project.

## Mechanical concept

- Mobile orchard base with two modeled drive wheels.
- Vertical lift mast with an 8 m simulated lift range.
- Six-joint manipulator.
- Adaptive harvest tool and servo-driven cutter.
- Perception stack designed for RGB-D, thermal, NIR and LiDAR sensing.
- Wrist force/torque and tool-current feedback for contact and jam detection.

## AI/control architecture

Sensors feed YOLO + SAM3 + tracking and a 3D tree/branch/fruit world model. Gemma 4 31B IT performs high-level reasoning and active-perception requests. GR00T, FLUX 3 Action and SmolVLA can propose candidate actions. A deterministic safety gate validates workspace, collision, human exclusion, joint limits, velocity, force/torque and emergency-stop conditions before ROS 2 / MoveIt 2 execution.

## Simulation

The URDF at robots/coconut_harvester.urdf is a lightweight reference model for Isaac Sim, Gazebo/ROS 2 and kinematic prototyping. It is not a certified mechanical design.

Recommended next step: import the URDF into the simulator, add a procedural coconut orchard, attach RGB-D/thermal/NIR/LiDAR sensors, and validate perception-to-action episodes before any real hardware deployment.

Real deployment requires mechanical/structural engineering, actuator sizing, guarding, braking, certified safety systems and controlled field validation.

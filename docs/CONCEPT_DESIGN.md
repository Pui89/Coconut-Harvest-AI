# Coconut Harvest Robot — Concept Design

**Project:** PUI89 AI Robotics  
**Status:** Engineering concept / simulation-first prototype  
**Repository:** https://github.com/Pui89/coconut-harvest-robot

## 1. Design objective

Develop an open-source, research-oriented system to assist coconut harvesting while reducing the need for people to climb trees. The initial target is a computer-only simulation and perception prototype. No claim is made that a physical robot can currently climb palms or safely cut coconuts.

## 2. Candidate mechanical architecture

The concept is a trunk-climbing robot with these subsystems:

1. **Adjustable trunk-grip frame:** opposing powered wheel or track modules; compliant contact pads; adjustable spacing for trunk diameter.
2. **Climbing drive:** independently controlled motors, encoder feedback, slip estimation, and a normally engaged brake or equivalent fail-safe.
3. **Perception mast:** RGB camera first; optional depth camera or LiDAR only when supported by hardware and testing.
4. **Harvesting arm:** compact articulated arm for positioning a guarded cutting end-effector near a detected bunch.
5. **Control and power module:** onboard computer, motor drivers, protected battery, emergency stop, telemetry, and service disconnect.
6. **Independent fall protection:** mechanical secondary retention and a rated tether for any physical prototype. Software alone is not fall protection.

The trunk-climbing configuration is a design hypothesis, not a settled design. A ground-based arm or assisted/manual platform should be compared against it before selecting hardware.

## 3. Operational concept

1. Inspect a simulated palm and identify trunk, fronds, bunches, and obstacles.
2. Estimate each candidate bunch's 3D location and uncertainty.
3. Rank targets using reachability and a configurable harvesting policy; do not infer ripeness unless a dataset and evaluation support it.
4. Check arm reach, collisions, trunk grip state, stability, and safety interlocks.
5. Request operator approval in early prototypes.
6. Execute a simulated approach, guarded cut, and retreat sequence.
7. Record outcome, failures, timing, target pose, software version, and test conditions.

If perception is uncertain, the target is unreachable, grip is lost, or a safety signal is missing, the system must stop and report **UNKNOWN / ABORT**, not continue automatically.

## 4. Simulation-first open-source stack

| Need | Candidate tool | Scope |
|---|---|---|
| Robot middleware | ROS 2 | Nodes, topics, services, lifecycle and diagnostics |
| Physics simulation | Gazebo Sim | Trunk, robot links, contact and motion experiments |
| Robot description | URDF / Xacro | Links, joints, inertias and visual/collision geometry |
| Vision | OpenCV; optional PyTorch | Image processing and model experiments |
| Manipulation planning | MoveIt 2, if arm model supports it | Reachability and collision-aware planning |
| CAD | FreeCAD | Editable mechanical concept |
| Testing | pytest + ROS 2 integration tests | Deterministic unit and scenario tests |
| Evidence | JSONL/CSV + scripts | Raw measurements, run metadata and summaries |

Tool selection must be confirmed against the developer's operating system and installed versions. Avoid adding heavyweight dependencies until the smallest testable milestone works.

## 5. Proposed development milestones

### M0 — Repository and model audit
- Inspect the current URDF, demo scripts, package metadata, and existing tests.
- Document what runs today versus what is proposed.
- Acceptance: clean environment setup instructions and a recorded baseline test result.

### M1 — Robot description
- Define trunk, grip modules, base frame, sensor frame, arm joints, and tool frame.
- Add realistic inertial and collision geometry; make dimensions configurable.
- Acceptance: model parses, frames are connected, joint limits are valid, and a visualization check is recorded.

### M2 — Palm test world
- Create a configurable trunk and a simple canopy/bunch target.
- Add scenarios for trunk diameter, friction, sensor noise, occlusion, and target location.
- Acceptance: scenario seeds and parameters are logged and repeatable.

### M3 — Perception baseline
- Start with synthetic labelled images or a clearly licensed, documented dataset.
- Measure precision, recall, localization error, and performance by lighting/occlusion condition.
- Acceptance: held-out evaluation with dataset provenance; no invented scores.

### M4 — Motion and safety supervisor
- Add reachability, collision checks, velocity/position limits, watchdogs, and explicit stop states.
- Acceptance: tests for unreachable targets, collision paths, lost perception, communication loss, and emergency-stop requests.

### M5 — Reproducible benchmark
- Publish raw run logs, configuration, software commit, simulator version, scenario seed, failures, and summary scripts.
- Acceptance: another developer can reproduce a reported result from documented commands.

### M6 — Physical feasibility review
- Only after simulation and risk review, evaluate a low-height, tethered, non-cutting test rig.
- Measure grip force, slip, brake stopping distance, structural loads, and power consumption before any tree-height trial.
- Do not test above people or operate a cutter until independent mechanical retention, emergency stopping, guarding, and a documented risk assessment are validated.

## 6. Benchmark protocol

Report at least:

- Target detection precision and recall on a held-out dataset
- 3D localization error in metres, including median and 95th percentile
- Reachability classification accuracy and false-safe rate
- Collision / safety-stop test outcomes
- Climb slip distance and stop distance in simulation; physical values only when measured on hardware
- Task completion rate, abort rate, and cycle time, with failure cases included
- Runtime environment, hardware, simulator version, configuration, random seeds, and raw data

Separate **design targets**, **simulation measurements**, and **physical measurements**. Never label a simulated result as a field result.

## 7. Safety boundaries

- Simulation and visualization are not evidence of safe physical operation.
- No human should be under the robot or falling-object path during testing.
- Use a guarded, non-powered mock end-effector during early physical experiments.
- Cutting requires a separate hazard analysis, mechanical guarding, positive interlocks, and a validated emergency-stop path.
- Loss of grip, power, communication, sensor validity, or localization must lead to a defined safe state.
- A tether is supplemental protection and must be engineered and rated for the actual load.

## 8. Definition of done for the first public milestone

- URDF loads with no parser errors.
- Simulation launch and teardown commands are documented.
- Automated tests pass in the stated environment.
- A short demo is explicitly labelled simulation.
- Benchmark logs include configuration and software revision.
- Limitations and unimplemented components remain visible in the README.

## 9. Current limitations

This document specifies a proposed architecture and acceptance criteria. It does not establish that autonomous climbing, coconut cutting, ripeness classification, field operation, or production readiness has been demonstrated. Those claims require measured evidence.

# PUI89 Full Robotics Stack Integration

This guide defines the full free/open-source stack as a staged, reviewable integration plan. Source scaffolding is present in this branch; no software is installed, no VLM weights are downloaded, and no physical system is connected or controlled.

## Stack choices

| System | Purpose | Cost and licence | Current status |
|---|---|---|---|
| ROS 2 Jazzy | Modular node/message layer | Open source; LTS support is published through May 2029. Ubuntu 24.04 is the recommended Tier 1 target. | A small optional Python bridge package is added; not built here. |
| Gazebo Harmonic | Physics/sensor simulation | Open source; check the licenses for individual plugins. Recommended companion for ROS 2 Jazzy on Ubuntu 24.04. | One starter SDF world is added per project; not yet a complete robot simulation. |
| Nav2 | Localisation, path planning and navigation for suitable mobile bases | Package licences vary: Apache-2.0, BSD-3-Clause and LGPL. Audit each selected package. | Documented next step only. The bridge does not issue Nav2 goals. |
| ArduPilot SITL | Optional software-in-the-loop autopilot for supported Copter, Plane, Rover and Sub classes | Free under GPLv3-or-later; read source and redistribution obligations. | Candidate for Flood Rescue only. Not installed or connected. |
| PX4 SITL | Alternative simulated autopilot, especially drone-oriented | Free under BSD-3-Clause; keep notices and licence text when redistributing. | Alternative to ArduPilot; do not integrate both in the first milestone. |
| SmolVLM-256M-Instruct | Exploratory image description / VLM smoke test | Publisher model card declares Apache-2.0. Main weights file is 513 MB; full repository listing is about 3.54 GB because of additional artifacts. | Offline-only smoke-test script added; no model is downloaded. |

Official references:
- ROS 2 Jazzy release/support: https://www.openrobotics.org/blog/2024/5/ros-jazzy-jalisco-released
- ROS/Gazebo compatibility: https://gazebosim.org/docs/harmonic/
- Nav2 component licences: https://github.com/ros-navigation/navigation2/blob/main/LICENSE
- ArduPilot SITL: https://ardupilot.ardupilot.org/dev/docs/sitl-simulator-software-in-the-loop.html
- ArduPilot GPLv3: https://docs.ardupilot.org/dev/docs/license-gplv3.html
- PX4 docs/licence: https://docs.px4.io/
- SmolVLM model and file list: https://huggingface.co/HuggingFaceTB/SmolVLM-256M-Instruct/tree/main
- SmolVLM main weights file: https://huggingface.co/HuggingFaceTB/SmolVLM-256M-Instruct/blob/main/model.safetensors

## Project-specific adoption

### Coconut Harvest AI
Use ROS 2 + Gazebo for a simplified orchard scene first. Nav2 may be added later for a simulated ground base only after a proper robot description, odometry, collision geometry and sensors exist. ArduPilot/PX4 are not needed in the initial orchard milestone. The VLM may describe a rights-cleared image but cannot decide maturity, a safe cutting point, or control a cutter.

### Extreme Flood Rescue AI
Use ROS 2 + Gazebo for repeatable scenes and then add a single simulated vehicle model. Nav2 is relevant only for a suitable ground/amphibious rover. Choose either ArduPilot SITL or PX4 SITL based on the first vehicle and licence requirements; do not install both at once. The included Gazebo world is dry terrain/obstacles only. The existing 0–15 m values are software scenario metadata, not simulated water pressure, currents, buoyancy or physical depth capability.

### Multimodal Narcotics Screening AI
Use ROS 2 + Gazebo for an indoor inspection base and mock sensors. Nav2 is a later mobile-base layer. Autopilot systems add no value to the first indoor milestone. SmolVLM output is descriptive free text and does not establish chemical identity, reveal closed-bag contents, or authorize accusation, search, detention, seizure or enforcement.

## ROS proposal bridge contract

The optional package lives under ros2/pui89_sim_bridge.

- Input: /pui89/sim/world_state as std_msgs/String containing JSON state.
- Output: /pui89/sim/action_proposal as std_msgs/String containing a JSON symbolic proposal and reason code.
- It has no cmd_vel publisher, no Nav2 goal publisher, no MAVLink client, no arming/motor/cutter command, and no enforcement interface.
- A SAFE_HOLD label from this node is a software proposal only. It is not a real emergency stop or physical safety controller.
- The dependency-free decision gate can be unit-tested without ROS installed. The actual ROS node requires a compatible ROS 2 Jazzy environment and is not covered by ordinary Python CI unless such an environment is separately configured.

## Local-only SmolVLM smoke test

The optional tool is tools/smolvlm_local_smoke_test.py. It requires an existing local model directory and an existing local image, forces Hugging Face offline flags, and passes local_files_only=True to model loaders. It never fetches missing model files. It records the prompt, input hash, weights hash, software/device context, observed latency and output. Model output is untrusted text for human review, never an actuator instruction.

Use the same local model folder across projects if you later decide to download it; do not download the full model repository three times. A model directory must contain its config, weights and processor/tokenizer assets. Missing files cause a local error rather than a download attempt.

## Platform and cost notes

The official recommended starting pairing is Ubuntu 24.04 + ROS 2 Jazzy + Gazebo Harmonic. Gazebo documentation describes Windows support as best-effort; do not assume that a native Windows setup works as smoothly as the primary Linux target. Before any install, record OS version, disk, available RAM and VRAM, then review the package/model licence. The source additions here do not change your computer and trigger no model or package downloads.

No paid API, paid cloud GPU, subscription or hosted inference is required by this scaffold. Open-source does not mean hardware, storage, setup, testing or legal review are cost-free.

## Implementation gates

1. Pass the existing standard-library tests and repeatable Python scenarios.
2. Parse/validate the starter SDF worlds and inspect the scene visually in the selected Gazebo version.
3. Build the ROS bridge only in a separate compatible ROS 2 workspace.
4. Add one robot model and its collision geometry/odometry/sensors; only then consider Nav2.
5. For Flood Rescue, choose one autopilot SITL only after the first vehicle model is in place.
6. Run SmolVLM only when complete local model files already exist and the operator explicitly chooses to run the smoke test.
7. Record real output and failures. Never label scaffolding as a measured benchmark or validated physical capability.

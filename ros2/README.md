# Optional ROS 2 workspace

The repository-root Python tests do not require ROS 2. For an actual ROS 2 build, use the documented compatibility target: Ubuntu 24.04 + ROS 2 Jazzy + Gazebo Harmonic. Check the official install instructions and licence notes linked from ../docs/PUI89_FULL_ROBOTICS_STACK_INTEGRATION.md.

From the repository root on a compatible machine:

```bash
source /opt/ros/jazzy/setup.bash
cd ros2
colcon build --packages-select pui89_sim_bridge
source install/setup.bash
ros2 run pui89_sim_bridge pui89_sim_proposal_bridge --ros-args -p project_id:=PUI89 -p ready_action:=REQUEST_HUMAN_REVIEW
```

In a separate terminal, publish one synthetic state object:

```bash
source /opt/ros/jazzy/setup.bash
source ros2/install/setup.bash
ros2 topic pub --once /pui89/sim/world_state std_msgs/msg/String "{data: '{"sensors_ok": true, "sensor_data_fresh": true, "comms_ok": true, "confidence": 0.9, "human_review_required": true}'}"
```

Observe the symbolic proposal:

```bash
ros2 topic echo /pui89/sim/action_proposal
```

The bridge outputs JSON labels only. It does not publish velocity, Nav2 goals, MAVLink, cutter, propulsion, door, alarm or enforcement commands. These commands are instructions for an operator to run manually after separately installing ROS 2; they are not run by CI or by this repository's source changes.

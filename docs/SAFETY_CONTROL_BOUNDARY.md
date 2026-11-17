# Safety Control Boundary

**AI proposes. Deterministic robotics validates. Safety controls.**

Future perception, reasoning and action models may provide evidence or candidate plans only. No detector is currently selected. The deterministic validator checks confidence, sensor health, workspace, collision state, exclusion zones, speed, force/torque limits, reachability and E-stop state.

Only the authorized robot-control stack may issue actuator commands. ROS 2 / MoveIt 2 are integration boundaries; actual hardware drivers, calibration, E-stop wiring and applicable safety validation remain hardware-specific.

Missing or contradictory sensor evidence must result in safe hold, abstention, replanning or human review rather than forced execution.
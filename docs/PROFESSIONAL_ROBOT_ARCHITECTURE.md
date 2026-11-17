# Professional Autonomous Coconut Harvesting Architecture

Sensors → calibration + synchronization → sensor health → future validated perception (not implemented) → segmentation/tracking → 3D/4D orchard world model → ripeness + harvestability evidence → reasoning → deterministic planning → human/policy review → deterministic safety gate → ROS 2 / MoveIt 2 boundary → validated controller → harvest verification → telemetry.

## Control boundary

AI models may generate evidence and candidate plans. They must not directly command motors, cutters, grippers, mobile bases, or emergency-stop behavior. Deterministic workspace, collision, exclusion-zone, joint-limit, force/torque, speed, sensor-health and E-stop checks remain authoritative.

## Professional maturity path

1. Reproducible recorded-data evaluation.
2. Sensor calibration and time synchronization.
3. 3D/4D target tracking.
4. Harvestability scoring with abstention.
5. Deterministic safety validation.
6. Simulation and hardware-in-the-loop.
7. ROS 2 / MoveIt 2 integration.
8. Operator dashboard and audit trail.
9. Field validation with measured KPIs.
10. Controlled deployment and maintenance lifecycle.

No field-success, latency, safety, yield, or productivity metric is claimed until measured on representative hardware/data.
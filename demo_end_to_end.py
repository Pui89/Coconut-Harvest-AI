"""Run a synthetic, safety-gated coconut-harvest pipeline demo.

This prints a JSON report only; it does not command robot hardware.
"""
from __future__ import annotations

import json

from coconut_harvest_robot.config import RobotConfig
from coconut_harvest_robot.data import SyntheticOrchard
from coconut_harvest_robot.end_to_end import run_end_to_end
from coconut_harvest_robot.harvestability import HarvestEvidence
from coconut_harvest_robot.safety_gate import ActionCandidate
from coconut_harvest_robot.sensor_quality import SensorObservation


def main() -> None:
    rgb = SyntheticOrchard.generate_rgb()
    depth = SyntheticOrchard.generate_depth()
    report = run_end_to_end(
        rgb=rgb,
        depth=depth,
        instruction="inspect candidate coconuts and propose a safe harvest plan",
        sensor_observations=[
            SensorObservation(name="rgb_camera", quality=1.0, timestamp_s=1.0),
            SensorObservation(name="depth_camera", quality=1.0, timestamp_s=1.01),
        ],
        evidence=HarvestEvidence(
            perception_confidence=0.90,
            localization_confidence=0.90,
            ripeness_confidence=0.90,
            reachability=0.90,
            collision_clearance_m=0.50,
            sensor_quality=1.0,
            occlusion=0.0,
            tracking_stability=0.90,
        ),
        candidate=ActionCandidate(
            target_id="synthetic-coconut-01",
            confidence=0.90,
            clearance_m=0.50,
            speed_mps=0.10,
            force_n=50.0,
            height_m=5.0,
            collision_free=False,
        ),
        collision_check_passed=False,
        config=RobotConfig(rrt_iterations=32),
    )
    print(json.dumps(report.to_dict(), indent=2))


if __name__ == "__main__":
    main()

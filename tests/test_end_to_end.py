import json

from coconut_harvest_robot.data import SyntheticOrchard
from coconut_harvest_robot.end_to_end import run_end_to_end
from coconut_harvest_robot.harvestability import HarvestEvidence
from coconut_harvest_robot.safety_gate import ActionCandidate
from coconut_harvest_robot.sensor_quality import SensorObservation


def _inputs():
    return dict(
        rgb=SyntheticOrchard.generate_rgb(height=32, width=32),
        depth=SyntheticOrchard.generate_depth(height=32, width=32),
        instruction="inspect the orchard",
        sensor_observations=[
            SensorObservation(name="rgb", quality=1.0, timestamp_s=1.0),
            SensorObservation(name="depth", quality=1.0, timestamp_s=1.01),
        ],
        evidence=HarvestEvidence(
            perception_confidence=0.95,
            localization_confidence=0.95,
            ripeness_confidence=0.95,
            reachability=0.95,
            collision_clearance_m=0.5,
            sensor_quality=1.0,
            occlusion=0.0,
            tracking_stability=0.95,
        ),
        candidate=ActionCandidate(
            target_id="test-target",
            confidence=0.95,
            clearance_m=0.5,
            speed_mps=0.1,
            force_n=50.0,
            height_m=5.0,
            collision_free=True,
        ),
    )


def test_end_to_end_blocks_unverified_path_and_never_sends_actuator_commands():
    report = run_end_to_end(**_inputs(), collision_check_passed=False)
    assert report.actuator_commands_sent is False
    assert report.trajectory_is_verified is False
    assert report.status == "BLOCKED"
    assert report.safety_decision == "BLOCK"
    assert any("collision validation" in reason for reason in report.safety_reasons)


def test_end_to_end_safe_holds_when_sensor_is_unsynchronized():
    args = _inputs()
    args["sensor_observations"] = [
        SensorObservation(name="rgb", quality=1.0, timestamp_s=1.0),
        SensorObservation(name="depth", quality=1.0, timestamp_s=1.5),
    ]
    report = run_end_to_end(**args, collision_check_passed=True)
    assert report.status == "SAFE_HOLD"
    assert report.actuator_commands_sent is False


def test_report_is_json_serializable():
    report = run_end_to_end(**_inputs(), collision_check_passed=False)
    encoded = json.dumps(report.to_dict())
    assert '"actuator_commands_sent": false' in encoded

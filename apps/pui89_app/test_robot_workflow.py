import json
import subprocess
import sys
from pathlib import Path

from apps.pui89_app.robot_workflow import Candidate, run_simulated_workflow

ROOT = Path(__file__).resolve().parents[2]


def good_candidate(**overrides):
    values = dict(
        target_id="coconut-01",
        confidence=0.9,
        bbox_xyxy_pixels=(10, 20, 50, 60),
        world_position_m=(1.0, 0.5, 1.2),
        localization_uncertainty_m=0.04,
        track_age_frames=8,
        timestamp_s=9.9,
        obstacle_clearance_m=0.5,
        reachable=True,
    )
    values.update(overrides)
    return Candidate(**values)


def test_no_candidates_abstains_in_safe_hold():
    report = run_simulated_workflow([], now_s=10)
    assert report.status == "SAFE_HOLD"
    assert report.selected_target_id is None
    assert report.actuator_commands_sent is False


def test_missing_3d_position_is_rejected_not_guessed():
    report = run_simulated_workflow(
        [good_candidate(world_position_m=None)], now_s=10, human_approved=True
    )
    assert report.status == "SAFE_HOLD"
    assert "METRIC_3D_POSITION_MISSING" in report.rejected_candidates["coconut-01"]


def test_stale_target_is_rejected():
    report = run_simulated_workflow(
        [good_candidate(timestamp_s=1.0)], now_s=10, human_approved=True
    )
    assert "DATA_STALE" in report.rejected_candidates["coconut-01"]


def test_invalid_box_is_rejected():
    report = run_simulated_workflow(
        [good_candidate(bbox_xyxy_pixels=(10, 20, 10, 60))], now_s=10
    )
    assert "BOUNDING_BOX_INVALID" in report.rejected_candidates["coconut-01"]


def test_non_numeric_box_is_rejected_without_crashing():
    report = run_simulated_workflow(
        [good_candidate(bbox_xyxy_pixels=(10, "not-a-number", 50, 60))], now_s=10
    )
    assert report.status == "SAFE_HOLD"
    assert "BOUNDING_BOX_INVALID" in report.rejected_candidates["coconut-01"]


def test_non_numeric_world_position_is_rejected_without_crashing():
    report = run_simulated_workflow(
        [good_candidate(world_position_m=(1.0, "unknown", 1.2))],
        now_s=10,
        human_approved=True,
    )
    assert report.status == "SAFE_HOLD"
    assert "METRIC_3D_POSITION_INVALID" in report.rejected_candidates["coconut-01"]


def test_emergency_stop_has_priority_over_candidates():
    report = run_simulated_workflow(
        [good_candidate()], now_s=10, human_approved=True, emergency_stop=True
    )
    assert report.status == "SAFE_HOLD"
    assert report.selected_target_id is None
    assert report.actuator_commands_sent is False


def test_human_approval_required_before_simulated_steps():
    report = run_simulated_workflow([good_candidate()], now_s=10)
    assert report.status == "AWAITING_HUMAN_APPROVAL"
    assert report.plan == []
    assert report.actuator_commands_sent is False


def test_approved_workflow_runs_simulated_steps_only():
    report = run_simulated_workflow(
        [good_candidate()], now_s=10, human_approved=True
    )
    assert report.status == "COMPLETED_SIMULATION"
    assert [step["action"] for step in report.plan] == [
        "APPROACH_PREVIEW", "HARVEST_TOOL_SEQUENCE_PREVIEW", "RETRACT_PREVIEW"
    ]
    assert report.actuator_commands_sent is False
    assert report.physical_harvest_verified is False
    assert report.state_history[-1] == "COMPLETED_SIMULATION"


def test_candidate_ranking_is_deterministic_and_reports_rejections():
    good = good_candidate(target_id="good")
    low_conf = good_candidate(target_id="low", confidence=0.3)
    report = run_simulated_workflow(
        [low_conf, good], now_s=10, human_approved=True
    )
    assert report.selected_target_id == "good"
    assert "DETECTION_CONFIDENCE_LOW" in report.rejected_candidates["low"]


def test_cli_emits_json_without_network_or_hardware():
    example = ROOT / "examples" / "end_to_end_robot_workflow.example.json"
    proc = subprocess.run(
        [sys.executable, "-m", "apps.pui89_app.run_robot_workflow", "--input", str(example)],
        cwd=ROOT, capture_output=True, text=True, check=True,
    )
    report = json.loads(proc.stdout)
    assert report["actuator_commands_sent"] is False
    assert report["physical_harvest_verified"] is False

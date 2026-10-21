"""Regression tests for the local-first coconut proposal safety boundary.

These tests exercise pure proposal/localization helpers and do not require a
trained model, a camera, a robot, or any network access.
"""
import numpy as np

from apps.pui89_app.local_first_pipeline import (
    Detection,
    Intrinsics,
    build_review_report,
    localize_detection,
)


def test_unknown_depth_rejects_candidate_and_never_authorizes_actuators():
    detection = Detection("coconut-001", 0.95, (10.0, 10.0, 30.0, 30.0))

    report = build_review_report([detection], {})

    assert report["candidate_count"] == 1
    assert report["candidates"][0]["status"] == "REJECTED"
    assert "3D location unavailable or invalid" in report["candidates"][0]["reasons"]
    assert report["actuator_commands_authorized"] is False
    assert report["robot_execution"] == "NOT_IMPLEMENTED"


def test_human_approval_only_marks_a_proposal_not_robot_execution():
    detection = Detection("coconut-001", 0.95, (10.0, 10.0, 30.0, 30.0))
    localized = {
        "coconut-001": {
            "status": "ESTIMATED_CAMERA_FRAME",
            "x_m": 0.1,
            "y_m": 0.1,
            "z_m": 1.0,
        }
    }

    report = build_review_report(
        [detection], localized, human_approved_target="coconut-001"
    )

    assert report["candidates"][0]["status"] == "HUMAN_APPROVED_PROPOSAL_ONLY"
    assert report["actuator_commands_authorized"] is False
    assert report["robot_execution"] == "NOT_IMPLEMENTED"


def test_camera_frame_localization_uses_valid_median_depth():
    detection = Detection("coconut-001", 0.9, (1.0, 1.0, 3.0, 3.0))
    depth = np.ones((5, 5), dtype=np.float32)
    intrinsics = Intrinsics(fx=100.0, fy=100.0, cx=2.0, cy=2.0)

    result = localize_detection(detection, depth, intrinsics)

    assert result["status"] == "ESTIMATED_CAMERA_FRAME"
    assert result["z_m"] == 1.0
    assert result["x_m"] == 0.0
    assert result["y_m"] == 0.0
    assert result["valid_depth_samples"] == 25


def test_invalid_depth_is_reported_as_unknown_not_fabricated_pose():
    detection = Detection("coconut-001", 0.9, (1.0, 1.0, 3.0, 3.0))
    depth = np.zeros((5, 5), dtype=np.float32)
    intrinsics = Intrinsics(fx=100.0, fy=100.0, cx=2.0, cy=2.0)

    result = localize_detection(detection, depth, intrinsics)

    assert result["status"] == "UNKNOWN"
    assert "no valid depth" in result["reason"]


# Local detector adapter regression tests. These use fakes and need no model weights.
from apps.pui89_app.local_detector import (
    coconut_class_ids,
    detect_coconuts,
    resolve_inference_device,
)


def test_coconut_class_ids_accepts_only_explicit_coconut_labels():
    assert coconut_class_ids({0: "person", 1: "coconut", 2: "green_coconut", 3: "coconuts"}) == {1, 3}


def test_device_resolution_is_deterministic_when_cuda_state_is_injected():
    assert resolve_inference_device("auto", cuda_available=False) == "cpu"
    assert resolve_inference_device("auto", cuda_available=True) == "0"
    assert resolve_inference_device("cpu", cuda_available=True) == "cpu"


def test_device_resolution_rejects_unknown_device():
    import pytest

    with pytest.raises(ValueError, match="device must be"):
        resolve_inference_device("tpu", cuda_available=False)


def test_detector_rejects_empty_class_set_before_model_call():
    import pytest

    with pytest.raises(ValueError, match="coconut class ID"):
        detect_coconuts(object(), object(), set(), device="cpu")


def test_detector_rejects_invalid_confidence_before_model_call():
    import pytest

    with pytest.raises(ValueError, match="confidence"):
        detect_coconuts(object(), object(), {0}, confidence=1.5, device="cpu")


def test_detector_returns_empty_list_when_model_has_no_results():
    class FakeModel:
        def predict(self, **kwargs):
            assert kwargs["device"] == "cpu"
            return []

    assert detect_coconuts(FakeModel(), object(), {0}, device="cpu") == []

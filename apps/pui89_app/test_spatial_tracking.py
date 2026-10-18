import math
import pytest

from apps.pui89_app.iou_tracker import Detection, IoUTracker, box_iou
from apps.pui89_app.rgbd_localization import CameraIntrinsics, estimate_xyz_from_bbox


def test_rgbd_localization_projects_median_depth_into_camera_frame():
    depth = [[2.0 for _ in range(20)] for _ in range(20)]
    estimate = estimate_xyz_from_bbox(
        depth, (4, 4, 16, 16),
        CameraIntrinsics(fx_px=10, fy_px=10, cx_px=10, cy_px=10),
    )
    assert estimate.camera_frame_xyz_m == pytest.approx((0.0, 0.0, 2.0))
    assert estimate.depth_mad_m == pytest.approx(0.0)
    assert estimate.valid_depth_samples > 5
    assert estimate.coordinate_frame == "camera"


def test_rgbd_localization_rejects_missing_or_invalid_depth():
    depth = [[float("nan") for _ in range(10)] for _ in range(10)]
    with pytest.raises(ValueError, match="insufficient valid depth"):
        estimate_xyz_from_bbox(
            depth, (1, 1, 9, 9),
            CameraIntrinsics(fx_px=5, fy_px=5, cx_px=5, cy_px=5),
        )


def test_rgbd_localization_rejects_bad_intrinsics_and_boxes():
    depth = [[1.0 for _ in range(10)] for _ in range(10)]
    with pytest.raises(ValueError, match="focal"):
        estimate_xyz_from_bbox(
            depth, (1, 1, 9, 9),
            CameraIntrinsics(fx_px=0, fy_px=5, cx_px=5, cy_px=5),
        )
    with pytest.raises(ValueError, match="bounding box"):
        estimate_xyz_from_bbox(
            depth, (8, 8, 12, 12),
            CameraIntrinsics(fx_px=5, fy_px=5, cx_px=5, cy_px=5),
        )


def test_iou_is_one_for_identical_boxes_and_zero_for_disjoint_boxes():
    assert box_iou((0, 0, 10, 10), (0, 0, 10, 10)) == pytest.approx(1)
    assert box_iou((0, 0, 10, 10), (20, 20, 30, 30)) == 0


def test_tracker_keeps_identity_for_overlapping_boxes_and_increments_age():
    tracker = IoUTracker(min_iou=0.2)
    first = tracker.update([Detection((0, 0, 10, 10), 0.9)])[0]
    second = tracker.update([Detection((1, 1, 11, 11), 0.8)])[0]
    assert second.track_id == first.track_id
    assert second.age_frames == 2


def test_tracker_creates_new_identity_for_non_overlapping_target():
    tracker = IoUTracker(min_iou=0.3)
    first = tracker.update([Detection((0, 0, 10, 10), 0.9)])[0]
    second = tracker.update([Detection((30, 30, 40, 40), 0.9)])[0]
    assert second.track_id != first.track_id

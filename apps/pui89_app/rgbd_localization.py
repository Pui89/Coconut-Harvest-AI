"""Small, dependency-free RGB-D bounding-box localization utility.

Requires a depth image aligned to RGB pixels, metric depth values in metres,
and calibrated pinhole camera intrinsics. Output coordinates are in the camera
frame, not the robot/world frame. It does not perform calibration or alignment.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from statistics import median
from typing import Sequence


@dataclass(frozen=True)
class CameraIntrinsics:
    fx_px: float
    fy_px: float
    cx_px: float
    cy_px: float


@dataclass(frozen=True)
class LocalizationEstimate:
    camera_frame_xyz_m: tuple[float, float, float]
    median_depth_m: float
    depth_mad_m: float
    valid_depth_samples: int
    coordinate_frame: str = "camera"


def estimate_xyz_from_bbox(
    depth_m: Sequence[Sequence[float]],
    bbox_xyxy_pixels: Sequence[float],
    intrinsics: CameraIntrinsics,
    *,
    min_depth_m: float = 0.10,
    max_depth_m: float = 15.0,
    min_valid_samples: int = 5,
) -> LocalizationEstimate:
    """Project the median valid depth at a box centre into camera-frame XYZ."""
    if not depth_m or not depth_m[0]:
        raise ValueError("depth image is empty")
    height, width = len(depth_m), len(depth_m[0])
    if any(len(row) != width for row in depth_m):
        raise ValueError("depth image rows must have equal width")
    values = (intrinsics.fx_px, intrinsics.fy_px, intrinsics.cx_px,
              intrinsics.cy_px, min_depth_m, max_depth_m)
    if not all(isfinite(float(v)) for v in values):
        raise ValueError("camera intrinsics and depth limits must be finite")
    if intrinsics.fx_px <= 0 or intrinsics.fy_px <= 0:
        raise ValueError("focal lengths must be positive")
    if min_depth_m <= 0 or max_depth_m <= min_depth_m:
        raise ValueError("depth limits are invalid")
    if len(bbox_xyxy_pixels) != 4 or not all(isfinite(float(v)) for v in bbox_xyxy_pixels):
        raise ValueError("bounding box must contain four finite pixel coordinates")
    x1, y1, x2, y2 = (float(v) for v in bbox_xyxy_pixels)
    if x1 < 0 or y1 < 0 or x2 <= x1 or y2 <= y1 or x2 > width or y2 > height:
        raise ValueError("bounding box is invalid or outside the depth image")
    if min_valid_samples < 1:
        raise ValueError("min_valid_samples must be positive")

    # Use the central half of the box to reduce contamination from background edges.
    left = max(0, int(x1 + (x2 - x1) * 0.25))
    right = min(width, int(x1 + (x2 - x1) * 0.75))
    top = max(0, int(y1 + (y2 - y1) * 0.25))
    bottom = min(height, int(y1 + (y2 - y1) * 0.75))
    samples: list[float] = []
    for row in depth_m[top:bottom]:
        for raw in row[left:right]:
            value = float(raw)
            if isfinite(value) and min_depth_m <= value <= max_depth_m:
                samples.append(value)
    if len(samples) < min_valid_samples:
        raise ValueError(
            f"insufficient valid depth samples: {len(samples)} < {min_valid_samples}"
        )
    z = median(samples)
    mad = median([abs(value - z) for value in samples])
    u, v = (x1 + x2) / 2.0, (y1 + y2) / 2.0
    x = (u - intrinsics.cx_px) * z / intrinsics.fx_px
    y = (v - intrinsics.cy_px) * z / intrinsics.fy_px
    return LocalizationEstimate(
        camera_frame_xyz_m=(x, y, z),
        median_depth_m=z,
        depth_mad_m=mad,
        valid_depth_samples=len(samples),
    )

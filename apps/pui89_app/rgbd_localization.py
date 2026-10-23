"""Small, dependency-free RGB-D bounding-box localization utility.

Requires a depth image aligned to RGB pixels, metric depth values in metres,
and calibrated pinhole camera intrinsics. Output coordinates are in the camera
frame, not the robot/world frame. It does not perform calibration or alignment.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from numbers import Real, Integral
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


def _finite_number(value: object, name: str) -> float:
    """Convert a real numeric input to a finite float or fail with context."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a finite numeric value")
    result = float(value)
    if not isfinite(result):
        raise ValueError(f"{name} must be a finite numeric value")
    return result


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
    try:
        height = len(depth_m)
        if height == 0:
            raise ValueError("depth image is empty")
        width = len(depth_m[0])
        if width == 0:
            raise ValueError("depth image is empty")
    except (TypeError, IndexError) as exc:
        raise ValueError("depth image must be a non-empty 2D sequence") from exc

    try:
        if any(len(row) != width for row in depth_m):
            raise ValueError("depth image rows must have equal width")
    except TypeError as exc:
        raise ValueError("depth image rows must be sequences") from exc

    fx = _finite_number(intrinsics.fx_px, "fx_px")
    fy = _finite_number(intrinsics.fy_px, "fy_px")
    cx = _finite_number(intrinsics.cx_px, "cx_px")
    cy = _finite_number(intrinsics.cy_px, "cy_px")
    min_depth = _finite_number(min_depth_m, "min_depth_m")
    max_depth = _finite_number(max_depth_m, "max_depth_m")
    if fx <= 0 or fy <= 0:
        raise ValueError("focal lengths must be positive")
    if min_depth <= 0 or max_depth <= min_depth:
        raise ValueError("depth limits are invalid")
    if (
        isinstance(min_valid_samples, bool)
        or not isinstance(min_valid_samples, Integral)
        or min_valid_samples < 1
    ):
        raise ValueError("min_valid_samples must be a positive integer")

    try:
        box = tuple(bbox_xyxy_pixels)
    except TypeError as exc:
        raise ValueError("bounding box must contain four finite pixel coordinates") from exc
    if len(box) != 4:
        raise ValueError("bounding box must contain four finite pixel coordinates")
    x1, y1, x2, y2 = (
        _finite_number(value, "bounding box coordinate") for value in box
    )
    if x1 < 0 or y1 < 0 or x2 <= x1 or y2 <= y1 or x2 > width or y2 > height:
        raise ValueError("bounding box is invalid or outside the depth image")

    # Use the central half of the box to reduce contamination from background edges.
    left = max(0, int(x1 + (x2 - x1) * 0.25))
    right = min(width, int(x1 + (x2 - x1) * 0.75))
    top = max(0, int(y1 + (y2 - y1) * 0.25))
    bottom = min(height, int(y1 + (y2 - y1) * 0.75))
    samples: list[float] = []
    for row in depth_m[top:bottom]:
        for raw in row[left:right]:
            if isinstance(raw, bool) or not isinstance(raw, Real):
                raise ValueError("depth image contains a non-numeric sample")
            value = float(raw)
            if isfinite(value) and min_depth <= value <= max_depth:
                samples.append(value)
    if len(samples) < min_valid_samples:
        raise ValueError(
            f"insufficient valid depth samples: {len(samples)} < {min_valid_samples}"
        )
    z = median(samples)
    mad = median([abs(value - z) for value in samples])
    u, v = (x1 + x2) / 2.0, (y1 + y2) / 2.0
    x = (u - cx) * z / fx
    y = (v - cy) * z / fy
    return LocalizationEstimate(
        camera_frame_xyz_m=(x, y, z),
        median_depth_m=z,
        depth_mad_m=mad,
        valid_depth_samples=len(samples),
    )

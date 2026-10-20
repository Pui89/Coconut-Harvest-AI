"""Local-only coconut image/depth inference to a reviewable harvest proposal.

No model downloads, hosted inference, cloud provisioning, or actuator commands.
Requires an existing local Ultralytics model with a class named coconut.
"""
from __future__ import annotations
import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

@dataclass(frozen=True)
class Detection:
    target_id: str
    confidence: float
    box_xyxy: tuple[float, float, float, float]
    class_name: str = "coconut"

@dataclass(frozen=True)
class Intrinsics:
    fx: float
    fy: float
    cx: float
    cy: float

def _positive(value: Any, name: str) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and greater than zero")
    return value

def load_intrinsics(path: str | Path) -> Intrinsics:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    cx, cy = float(raw["cx"]), float(raw["cy"])
    if not math.isfinite(cx) or not math.isfinite(cy):
        raise ValueError("cx and cy must be finite")
    return Intrinsics(_positive(raw["fx"], "fx"), _positive(raw["fy"], "fy"), cx, cy)

def load_local_detector(weights_path: str | Path):
    """Load only an existing local weights file; never download weights."""
    path = Path(weights_path).expanduser()
    if not path.is_file() or path.suffix.lower() not in {".pt", ".pth"}:
        raise FileNotFoundError("Supply an existing local .pt/.pth file; no download is attempted.")
    try:
        from ultralytics import YOLO
    except ImportError as exc:
        raise RuntimeError("Ultralytics is optional and not installed; install it manually if wanted.") from exc
    model = YOLO(str(path))
    names = getattr(model, "names", {})
    values = names.values() if isinstance(names, dict) else names
    if not any(str(name).strip().casefold() == "coconut" for name in values):
        raise ValueError("Model has no class named 'coconut'; refusing to relabel another class.")
    return model

def run_local_detector(model: Any, image_path: str | Path, confidence: float = 0.35) -> list[Detection]:
    image = Path(image_path).expanduser()
    if not image.is_file():
        raise FileNotFoundError(f"Image not found: {image}")
    if not math.isfinite(confidence) or not 0 <= confidence <= 1:
        raise ValueError("confidence must be finite and in [0, 1]")
    results = model.predict(source=str(image), conf=confidence, verbose=False)
    found: list[Detection] = []
    for result in results:
        names, boxes = result.names, getattr(result, "boxes", None)
        if boxes is None:
            continue
        for box in boxes:
            cls_id = int(box.cls.item())
            name = names[cls_id] if isinstance(names, dict) else names[cls_id]
            if str(name).strip().casefold() != "coconut":
                continue
            score = float(box.conf.item())
            coords = tuple(float(v) for v in box.xyxy[0].tolist())
            if len(coords) != 4 or not all(math.isfinite(v) for v in coords):
                continue
            if not math.isfinite(score) or not 0 <= score <= 1:
                continue
            found.append(Detection(f"coconut-{len(found)+1:03d}", score, coords))  # type: ignore[arg-type]
    return found

def localize_detection(detection: Detection, depth_map: Any, intrinsics: Intrinsics, *,
                       depth_scale: float = 1.0, min_depth_m: float = 0.15,
                       max_depth_m: float = 5.0, window_radius: int = 2) -> dict[str, Any]:
    """Median-depth pinhole projection to camera-frame XYZ; not world-frame pose."""
    import numpy as np
    if getattr(depth_map, "ndim", None) != 2 or not np.issubdtype(depth_map.dtype, np.number):
        raise ValueError("depth map must be a 2-D numeric array")
    scale = _positive(depth_scale, "depth_scale")
    if (not math.isfinite(min_depth_m) or not math.isfinite(max_depth_m)
            or min_depth_m <= 0 or max_depth_m <= min_depth_m):
        raise ValueError("depth bounds must be finite, positive, and ordered")
    h, w = depth_map.shape
    x1, y1, x2, y2 = detection.box_xyxy
    u, v = int(round((x1+x2)/2)), int(round((y1+y2)/2))
    if not (0 <= u < w and 0 <= v < h):
        return {"status": "UNKNOWN", "reason": "box centre outside depth image"}
    r = max(0, int(window_radius))
    patch = depth_map[max(0,v-r):min(h,v+r+1), max(0,u-r):min(w,u+r+1)].astype(float) * scale
    valid = patch[np.isfinite(patch) & (patch >= min_depth_m) & (patch <= max_depth_m)]
    if valid.size == 0:
        return {"status": "UNKNOWN", "reason": "no valid depth near target centre"}
    z = float(np.median(valid))
    return {"status": "ESTIMATED_CAMERA_FRAME",
            "x_m": round((u-intrinsics.cx)*z/intrinsics.fx, 5),
            "y_m": round((v-intrinsics.cy)*z/intrinsics.fy, 5),
            "z_m": round(z, 5), "pixel_uv": [u,v],
            "valid_depth_samples": int(valid.size),
            "note": "Camera-frame estimate only; calibration/alignment require validation."}

def build_review_report(detections: list[Detection], localized: dict[str, dict[str, Any]], *,
                        min_confidence: float = 0.60, min_range_m: float = 0.15,
                        max_range_m: float = 3.0, human_approved_target: str | None = None) -> dict[str, Any]:
    if not math.isfinite(min_confidence) or not 0 <= min_confidence <= 1:
        raise ValueError("min_confidence must be finite and in [0, 1]")
    if not (math.isfinite(min_range_m) and math.isfinite(max_range_m)
            and 0 < min_range_m < max_range_m):
        raise ValueError("range limits must be finite, positive, and ordered")
    candidates = []
    for det in detections:
        reasons = []
        if det.class_name.strip().casefold() != "coconut":
            reasons.append("class is not coconut")
        loc = localized.get(det.target_id, {"status":"UNKNOWN", "reason":"depth unavailable"})
        if not math.isfinite(det.confidence) or not 0 <= det.confidence <= 1:
            reasons.append("invalid confidence")
        elif det.confidence < min_confidence:
            reasons.append("confidence below configured threshold")
        if loc.get("status") != "ESTIMATED_CAMERA_FRAME":
            reasons.append("3D location unavailable or invalid")
        else:
            try:
                xyz = tuple(float(loc[k]) for k in ("x_m", "y_m", "z_m"))
                distance = math.sqrt(sum(value * value for value in xyz))
            except (KeyError, TypeError, ValueError, OverflowError):
                distance = math.nan
            if not math.isfinite(distance):
                reasons.append("3D coordinates are missing or non-finite")
            elif not min_range_m <= distance <= max_range_m:
                reasons.append("target outside configured camera-frame range")
        status = "REJECTED" if reasons else "REVIEW_REQUIRED"
        if not reasons and human_approved_target == det.target_id:
            status = "HUMAN_APPROVED_PROPOSAL_ONLY"
        candidates.append({"target_id":det.target_id, "confidence":round(det.confidence,5),
                           "box_xyxy":list(det.box_xyxy), "localization":loc,
                           "status":status, "reasons":reasons})
    candidates.sort(key=lambda x: (-x["confidence"], x["target_id"]))
    return {"schema_version":"1.0", "mode":"LOCAL_ONLY_PROPOSAL",
            "candidate_count":len(candidates), "candidates":candidates,
            "human_approved_target":human_approved_target,
            "actuator_commands_authorized":False, "robot_execution":"NOT_IMPLEMENTED",
            "safety_notice":"Proposal only: no world transform, reachability solver, full-volume collision check, or physical safety validation. Never connect this report directly to actuators."}

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weights", required=True, help="Existing local coconut .pt/.pth file")
    parser.add_argument("--image", required=True, help="Local RGB image")
    parser.add_argument("--depth-npy", required=True, help="Aligned local 2-D depth .npy")
    parser.add_argument("--intrinsics-json", required=True, help="JSON with fx, fy, cx, cy")
    parser.add_argument("--depth-scale", type=float, default=1.0, help="Convert raw depth to metres")
    parser.add_argument("--confidence", type=float, default=0.35)
    parser.add_argument("--min-target-confidence", type=float, default=0.60)
    parser.add_argument("--human-approved-target", help="Record human review only; does not run robot")
    parser.add_argument("--output", default="coconut_robot_proposal.json")
    args = parser.parse_args(argv)
    import numpy as np
    model = load_local_detector(args.weights)
    detections = run_local_detector(model, args.image, args.confidence)
    depth = np.load(args.depth_npy, allow_pickle=False)
    if depth.ndim != 2 or not np.issubdtype(depth.dtype, np.number):
        raise ValueError("depth file must contain a numeric 2-D array")
    # A detector box is expressed in RGB-image pixels. Refuse to project it
    # into a depth map with a different raster size unless the caller explicitly
    # preprocesses both into a validated, aligned coordinate system beforehand.
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("Pillow is required to verify RGB/depth dimensions.") from exc
    with Image.open(args.image) as rgb_image:
        rgb_width, rgb_height = rgb_image.size
    if depth.shape != (rgb_height, rgb_width):
        raise ValueError(
            f"RGB/depth dimensions do not match: RGB is {rgb_width}x{rgb_height}, "
            f"depth is {depth.shape[1]}x{depth.shape[0]}. Align/resize the depth map "
            "using a documented sensor pipeline before localization; no automatic "
            "resizing is performed."
        )
    intrinsics = load_intrinsics(args.intrinsics_json)
    localized = {d.target_id:localize_detection(d, depth, intrinsics, depth_scale=args.depth_scale)
                 for d in detections}
    report = build_review_report(detections, localized,
              min_confidence=args.min_target_confidence,
              human_approved_target=args.human_approved_target)
    Path(args.output).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"output":args.output, "candidate_count":report["candidate_count"],
                      "actuator_commands_authorized":False}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

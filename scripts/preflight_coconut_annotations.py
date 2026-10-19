#!/usr/bin/env python3
"""Preflight coconut detection annotations without changing or inventing labels.

Uses only the Python standard library. This validates normalized XYWH geometry and
reports overlaps as review flags, not automatic annotation errors. It deliberately
does not train a detector or approve image licensing.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_annotations(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict) or not isinstance(data.get("images"), list):
        raise ValueError("Expected a JSON object with an 'images' list")
    return data


def box_iou(a: dict[str, float], b: dict[str, float]) -> float:
    ax1, ay1 = a["x"], a["y"]
    ax2, ay2 = ax1 + a["w"], ay1 + a["h"]
    bx1, by1 = b["x"], b["y"]
    bx2, by2 = b["x"] + b["w"], b["y"] + b["h"]
    iw = max(0.0, min(ax2, bx2) - max(ax1, bx1))
    ih = max(0.0, min(ay2, by2) - max(ay1, by1))
    inter = iw * ih
    union = a["w"] * a["h"] + b["w"] * b["h"] - inter
    return inter / union if union > 0 else 0.0


def audit(data: dict[str, Any], overlap_threshold: float = 0.15) -> list[str]:
    issues: list[str] = []
    images = data["images"]
    seen: set[str] = set()
    total_boxes = 0

    for image in images:
        name = str(image.get("filename", "<missing filename>"))
        if name in seen:
            issues.append(f"ERROR {name}: duplicate image record")
        seen.add(name)
        width, height = image.get("width"), image.get("height")
        if not isinstance(width, int) or width <= 0 or not isinstance(height, int) or height <= 0:
            issues.append(f"ERROR {name}: width and height must be positive integers")
        boxes = image.get("boxes")
        if not isinstance(boxes, list):
            issues.append(f"ERROR {name}: boxes must be a list")
            continue
        total_boxes += len(boxes)
        valid_boxes: list[tuple[int, dict[str, float]]] = []
        for index, box in enumerate(boxes, start=1):
            if not isinstance(box, dict) or any(k not in box for k in ("x", "y", "w", "h")):
                issues.append(f"ERROR {name} box {index}: missing x/y/w/h")
                continue
            try:
                x, y, w, h = (float(box[k]) for k in ("x", "y", "w", "h"))
            except (TypeError, ValueError):
                issues.append(f"ERROR {name} box {index}: coordinates must be numeric")
                continue
            if w <= 0 or h <= 0:
                issues.append(f"ERROR {name} box {index}: width and height must be positive")
                continue
            if x < 0 or y < 0 or x + w > 1.000001 or y + h > 1.000001:
                issues.append(f"ERROR {name} box {index}: normalized box lies outside image")
                continue
            if x <= 0.002 or y <= 0.002 or x + w >= 0.998 or y + h >= 0.998:
                issues.append(f"REVIEW {name} box {index}: touches image boundary; check truncation policy")
            valid_boxes.append((index, {"x": x, "y": y, "w": w, "h": h}))

        for pos, (idx_a, box_a) in enumerate(valid_boxes):
            for idx_b, box_b in valid_boxes[pos + 1:]:
                overlap = box_iou(box_a, box_b)
                if overlap >= overlap_threshold:
                    issues.append(
                        f"REVIEW {name} boxes {idx_a}/{idx_b}: IoU={overlap:.3f}; "
                        "overlap is a review flag, not proof of an error"
                    )

    errors = sum(line.startswith("ERROR ") for line in issues)
    reviews = sum(line.startswith("REVIEW ") for line in issues)
    print(f"Images: {len(images)} | Boxes: {total_boxes} | Errors: {errors} | Review flags: {reviews}")
    for issue in issues:
        print(issue)
    if not issues:
        print("Geometry preflight passed. This does not verify visual correctness, recall, or image reuse rights.")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--annotations",
        type=Path,
        default=Path("data/review_batch_2026-10-18/annotations_v0.1.json"),
    )
    parser.add_argument("--overlap-threshold", type=float, default=0.15)
    args = parser.parse_args()
    if not 0.0 <= args.overlap_threshold <= 1.0:
        parser.error("--overlap-threshold must be between 0 and 1")
    try:
        issues = audit(load_annotations(args.annotations), args.overlap_threshold)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Preflight failed: {exc}", file=sys.stderr)
        return 2
    return 1 if any(issue.startswith("ERROR ") for issue in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())

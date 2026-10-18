#!/usr/bin/env python3
"""Dependency-free geometry audit for normalized coconut bounding boxes.

This tool does not determine whether a box matches a real coconut. It flags
geometry conditions for human review and deliberately does not edit annotations.
"""
from __future__ import annotations
import argparse
import json
from itertools import combinations
from pathlib import Path


def box_iou(a: dict, b: dict) -> float:
    ax1, ay1 = float(a["x"]), float(a["y"])
    ax2, ay2 = ax1 + float(a["w"]), ay1 + float(a["h"])
    bx1, by1 = float(b["x"]), float(b["y"])
    bx2, by2 = bx1 + float(b["w"]), by1 + float(b["h"])
    iw = max(0.0, min(ax2, bx2) - max(ax1, bx1))
    ih = max(0.0, min(ay2, by2) - max(ay1, by1))
    inter = iw * ih
    union = float(a["w"]) * float(a["h"]) + float(b["w"]) * float(b["h"]) - inter
    return inter / union if union > 0 else 0.0


def audit(path: Path, overlap_threshold: float) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    results = []
    for image in payload.get("images", []):
        filename = image.get("filename", "<missing filename>")
        boxes = image.get("boxes", [])
        errors, warnings = [], []
        for idx, box in enumerate(boxes, start=1):
            try:
                x, y, w, h = (float(box[k]) for k in ("x", "y", "w", "h"))
            except (KeyError, TypeError, ValueError) as exc:
                errors.append({"box": idx, "issue": f"missing_or_non_numeric_coordinate: {exc}"})
                continue
            if w <= 0 or h <= 0:
                errors.append({"box": idx, "issue": "non_positive_width_or_height"})
            if x < 0 or y < 0 or x + w > 1 or y + h > 1:
                errors.append({"box": idx, "issue": "box_outside_normalized_image_bounds"})
            if any(abs(v) < 1e-9 for v in (x, y)) or abs(x + w - 1) < 1e-9 or abs(y + h - 1) < 1e-9:
                warnings.append({"box": idx, "issue": "touches_image_border; review truncated-object policy"})
        overlaps = []
        for (i, a), (j, b) in combinations(list(enumerate(boxes, start=1)), 2):
            try:
                score = box_iou(a, b)
            except (KeyError, TypeError, ValueError):
                continue
            if score >= overlap_threshold:
                overlaps.append({"boxes": [i, j], "iou": round(score, 6),
                                 "issue": "overlap_review_flag_not_automatic_error"})
        results.append({
            "filename": filename,
            "box_count": len(boxes),
            "errors": errors,
            "border_warnings": warnings,
            "overlap_warnings": overlaps,
            "status": "geometry_error" if errors else ("review_warnings" if warnings or overlaps else "geometry_checks_passed"),
            "human_visual_qa": "not_automated"
        })
    return {
        "format": "pui89-coconut-annotation-geometry-audit-v1",
        "annotation_file": str(path),
        "overlap_iou_warning_threshold": overlap_threshold,
        "image_count": len(results),
        "box_count": sum(x["box_count"] for x in results),
        "geometry_error_count": sum(len(x["errors"]) for x in results),
        "images": results,
        "interpretation": "Geometry checks cannot confirm missed fruit or correct boundaries. Human visual review and licence clearance remain required."
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--annotations", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--overlap-iou-warning", type=float, default=0.15)
    args = parser.parse_args()
    report = audit(args.annotations, args.overlap_iou_warning)
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 1 if report["geometry_error_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

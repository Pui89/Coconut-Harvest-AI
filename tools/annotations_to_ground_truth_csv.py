#!/usr/bin/env python3
"""Export PUI89 normalized annotation JSON to the detection evaluator's pixel CSV.

This is a format converter, not an annotation QA system. It requires an explicit
human-QA acknowledgement before writing evaluator-ready ground truth.
Standard-library only; it does not run a detector or calculate metrics.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path
from typing import Any

FORMAT = "pui89-coconut-annotations-v1"
CSV_FIELDS = ["image_id", "xmin", "ymin", "xmax", "ymax", "class"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--annotations", required=True, type=Path,
                        help="JSON exported by tools/coconut_annotator.html")
    parser.add_argument("--output", required=True, type=Path,
                        help="Destination ground-truth CSV (created only after validation)")
    parser.add_argument("--images-dir", type=Path,
                        help="Optional directory; require every annotated image file to exist")
    parser.add_argument("--confirm-human-qa", action="store_true",
                        help="A human has inspected full-resolution overlays and independently reviewed labels")
    parser.add_argument("--summary", type=Path,
                        help="Optional JSON summary path")
    return parser.parse_args()


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def convert(payload: Any, images_dir: Path | None, confirm_human_qa: bool) -> tuple[list[dict[str, str]], dict]:
    if not isinstance(payload, dict) or payload.get("format") != FORMAT:
        raise ValueError(f"expected annotation JSON format {FORMAT!r}")
    images = payload.get("images")
    if not isinstance(images, list) or not images:
        raise ValueError("annotation JSON must contain a non-empty 'images' list")

    rows: list[dict[str, str]] = []
    seen_names: set[str] = set()
    total_boxes = 0
    for image_index, image in enumerate(images, start=1):
        if not isinstance(image, dict):
            raise ValueError(f"images[{image_index - 1}] must be an object")
        filename = image.get("filename")
        if not isinstance(filename, str) or not filename.strip():
            raise ValueError(f"images[{image_index - 1}] has no filename")
        filename = filename.strip()
        if Path(filename).name != filename or filename in {".", ".."}:
            raise ValueError(f"image filename must be a basename, not a path: {filename!r}")
        folded = filename.casefold()
        if folded in seen_names:
            raise ValueError(f"duplicate image filename: {filename!r}")
        seen_names.add(folded)

        width, height = image.get("width"), image.get("height")
        if not finite_number(width) or not finite_number(height) or width <= 0 or height <= 0:
            raise ValueError(f"{filename}: width and height must be positive finite numbers")
        if int(width) != width or int(height) != height:
            raise ValueError(f"{filename}: image width and height must be integers")
        if images_dir is not None and not (images_dir / filename).is_file():
            raise ValueError(f"{filename}: image file not found under {images_dir}")

        boxes = image.get("boxes")
        if not isinstance(boxes, list):
            raise ValueError(f"{filename}: boxes must be a list")
        for box_index, box in enumerate(boxes, start=1):
            if not isinstance(box, dict):
                raise ValueError(f"{filename}: box {box_index} must be an object")
            if not all(finite_number(box.get(k)) for k in ("x", "y", "w", "h")):
                raise ValueError(f"{filename}: box {box_index} coordinates must be finite numbers")
            x, y, w, h = (float(box[k]) for k in ("x", "y", "w", "h"))
            if w <= 0 or h <= 0 or x < 0 or y < 0 or x + w > 1.000001 or y + h > 1.000001:
                raise ValueError(f"{filename}: box {box_index} is outside normalized image bounds")
            # Clamp tiny floating-point overshoot accepted by the tolerance above.
            x1, y1 = max(0.0, x), max(0.0, y)
            x2, y2 = min(1.0, x + w), min(1.0, y + h)
            row = {
                "image_id": filename,
                "xmin": str(round(x1 * int(width), 4)),
                "ymin": str(round(y1 * int(height), 4)),
                "xmax": str(round(x2 * int(width), 4)),
                "ymax": str(round(y2 * int(height), 4)),
                "class": "coconut",
            }
            rows.append(row)
            total_boxes += 1

    summary = {
        "schema": "pui89-annotation-to-ground-truth-conversion-v1",
        "annotation_format": FORMAT,
        "image_count": len(images),
        "box_count": total_boxes,
        "images_with_zero_boxes": sum(not item["boxes"] for item in images),
        "human_qa_acknowledged": confirm_human_qa,
        "evaluator_csv_written": confirm_human_qa,
        "limitations": [
            "This conversion checks structure and box geometry only; it cannot verify that boxes match real coconuts.",
            "Human QA acknowledgement is supplied by the operator and is not independently verified by this script.",
            "Image dimensions come from the annotation export; --images-dir checks file existence, not image dimensions.",
            "The output is ground truth only. Detector predictions must come from an actual inference run on the same held-out images.",
            "Image rights, split integrity, and source-group independence require separate review."
        ]
    }
    return rows, summary


def main() -> int:
    args = parse_args()
    if not args.annotations.is_file():
        print(f"ERROR: annotations file not found: {args.annotations}", file=sys.stderr)
        return 2
    try:
        payload = json.loads(args.annotations.read_text(encoding="utf-8"))
        rows, summary = convert(payload, args.images_dir, args.confirm_human_qa)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if not args.confirm_human_qa:
        print(json.dumps(summary, indent=2))
        print("NOT WRITTEN: inspect full-resolution overlays and obtain independent human label QA, then rerun with --confirm-human-qa.", file=sys.stderr)
        return 3

    args.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with args.output.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        if args.summary:
            args.summary.parent.mkdir(parents=True, exist_ok=True)
            args.summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: could not write output: {exc}", file=sys.stderr)
        return 2

    print(json.dumps({**summary, "output_csv": str(args.output), "summary_json": str(args.summary) if args.summary else None}, indent=2))
    print("Ground-truth CSV created. This does not establish dataset rights, split validity, or detector performance.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

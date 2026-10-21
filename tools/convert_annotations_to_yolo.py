#!/usr/bin/env python3
"""Convert PUI89 offline annotator JSON into YOLO detection label files.

The annotator stores normalized boxes as top-left x/y plus width/height.
YOLO stores class_id, center_x, center_y, width, height, all normalized.
This converter does not split datasets, download images, or train a model.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--annotations", required=True, type=Path, help="coconut-annotations.json exported by coconut_annotator.html")
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory where labels/ and conversion_summary.json will be written")
    parser.add_argument("--images-dir", type=Path, help="Optional directory containing the original images; checks that each named image exists")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.annotations.is_file():
        print(f"ERROR: annotations file not found: {args.annotations}", file=sys.stderr)
        return 2
    try:
        payload = json.loads(args.annotations.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: could not read valid JSON: {exc}", file=sys.stderr)
        return 2

    if not isinstance(payload, dict):
        print("ERROR: annotation JSON top level must be an object.", file=sys.stderr)
        return 2

    if payload.get("format") != "pui89-coconut-annotations-v1":
        print("ERROR: unsupported annotation format; export JSON from the PUI89 annotator.", file=sys.stderr)
        return 2
    images = payload.get("images")
    if not isinstance(images, list) or not images:
        print("ERROR: JSON contains no images.", file=sys.stderr)
        return 2

    args.output_dir.mkdir(parents=True, exist_ok=True)
    labels_dir = args.output_dir / "labels"
    labels_dir.mkdir(parents=True, exist_ok=True)
    seen_stems: set[str] = set()
    summary_rows = []
    total_boxes = 0
    skipped_empty = 0

    for record_index, item in enumerate(images, start=1):
        if not isinstance(item, dict):
            print(f"ERROR: image record {record_index} must be an object.", file=sys.stderr)
            return 2
        filename = item.get("filename")
        boxes = item.get("boxes", [])
        if not isinstance(boxes, list):
            print("ERROR: boxes for image record must be a list.", file=sys.stderr)
            return 2
        if not isinstance(filename, str) or not filename:
            print("ERROR: an image record has no filename.", file=sys.stderr)
            return 2
        image_path = (args.images_dir / filename) if args.images_dir else None
        if image_path is not None and not image_path.is_file():
            print(f"ERROR: image file named in JSON is missing: {image_path}", file=sys.stderr)
            return 2

        stem = Path(filename).stem
        if stem in seen_stems:
            print(f"ERROR: duplicate filename stem '{stem}'. Rename images so every image has a unique basename before converting.", file=sys.stderr)
            return 2
        seen_stems.add(stem)
        lines = []
        for index, box in enumerate(boxes, start=1):
            try:
                x, y, w, h = (float(box[k]) for k in ("x", "y", "w", "h"))
            except (KeyError, TypeError, ValueError):
                print(f"ERROR: invalid box {index} in {filename}.", file=sys.stderr)
                return 2
            values = (x, y, w, h)
            if not all(0.0 <= v <= 1.0 for v in values) or w <= 0 or h <= 0 or x + w > 1.000001 or y + h > 1.000001:
                print(f"ERROR: box {index} in {filename} is outside normalized image bounds.", file=sys.stderr)
                return 2
            cx, cy = x + w / 2.0, y + h / 2.0
            lines.append(f"0 {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")
        label_path = labels_dir / f"{stem}.txt"
        label_path.write_text(("\n".join(lines) + "\n") if lines else "", encoding="utf-8")
        if not lines:
            skipped_empty += 1
        total_boxes += len(lines)
        summary_rows.append({"filename": filename, "label_file": str(label_path.relative_to(args.output_dir)), "coconut_boxes": len(lines), "has_positive_label": bool(lines)})

    report = {
        "format": "pui89-yolo-conversion-summary-v1",
        "source_annotations": str(args.annotations),
        "images_dir_checked": str(args.images_dir) if args.images_dir else None,
        "class_names": ["coconut"],
        "class_id": 0,
        "image_count": len(summary_rows),
        "images_with_boxes": sum(row["has_positive_label"] for row in summary_rows),
        "images_without_boxes": skipped_empty,
        "total_boxes": total_boxes,
        "records": summary_rows,
        "warning": "Conversion validates label format only. It does not verify annotation quality, licence compliance, dataset independence, or model performance."
    }
    report_path = args.output_dir / "conversion_summary.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Converted {len(summary_rows)} image records and {total_boxes} coconut boxes.")
    print(f"YOLO labels: {labels_dir}")
    print(f"Summary: {report_path}")
    print("Next: place images and labels into separate train/val/test folders grouped by tree or capture session.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Render normalized coconut boxes over source images for human annotation QA.

This script visualizes labels only; it does not verify box correctness, detect
missed fruit, or clear image licences. Use only locally available images whose
reuse terms have been checked. Archived labels should remain excluded from training.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--images-dir", required=True, type=Path,
                        help="Directory containing original images named in the annotation JSON")
    parser.add_argument("--annotations", required=True, type=Path,
                        help="JSON file with normalized x/y/w/h boxes")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--banner", default="ANNOTATION REVIEW ONLY",
                        help="Visible warning printed at the top of every rendered image")
    args = parser.parse_args()

    payload = json.loads(args.annotations.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    failures = 0

    for item in payload.get("images", []):
        filename = item.get("filename")
        if not filename:
            print("SKIP: annotation entry has no filename")
            failures += 1
            continue
        source = args.images_dir / filename
        image = cv2.imread(str(source))
        if image is None:
            print(f"MISSING/UNREADABLE: {source}")
            failures += 1
            continue

        height, width = image.shape[:2]
        for index, box in enumerate(item.get("boxes", []), start=1):
            try:
                x = float(box["x"])
                y = float(box["y"])
                w = float(box["w"])
                h = float(box["h"])
            except (KeyError, TypeError, ValueError) as exc:
                print(f"INVALID BOX: {filename} box {index}: {exc}")
                failures += 1
                continue

            x1 = round(x * width)
            y1 = round(y * height)
            x2 = round((x + w) * width)
            y2 = round((y + h) * height)
            valid = (0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height)
            if not valid:
                print(f"OUT-OF-BOUNDS BOX: {filename} box {index}")
                failures += 1
                continue

            cv2.rectangle(image, (x1, y1), (x2, y2), (40, 220, 40), 2)
            cv2.putText(image, f"GT {index}", (x1, max(18, y1 - 5)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (40, 220, 40), 2,
                        cv2.LINE_AA)

        banner = args.banner[:100]
        cv2.rectangle(image, (0, 0), (width, min(38, height)), (20, 20, 20), -1)
        cv2.putText(image, banner, (8, min(26, height - 2)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.62, (255, 255, 255), 2,
                    cv2.LINE_AA)
        destination = args.output_dir / f"{Path(filename).stem}_annotation-review.jpg"
        if not cv2.imwrite(str(destination), image):
            print(f"WRITE FAILED: {destination}")
            failures += 1
        else:
            print(f"WROTE: {destination}")

    print(f"Finished. Entries with missing files or invalid boxes: {failures}")
    print("Human visual review is still required; rendered boxes are not validated labels.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

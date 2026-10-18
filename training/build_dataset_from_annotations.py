#!/usr/bin/env python3
"""Build a licence-reviewed, group-split YOLO dataset from PUI89 annotations.

This tool does not download images, create labels, or certify label correctness.
It requires a human review CSV and Commons provenance for every image.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
SPLITS = ("train", "val", "test")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv(path: Path, required: set[str]) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError(f"{path} must contain columns: {', '.join(sorted(required))}")
        return [{str(k): (v or "").strip() for k, v in row.items()} for row in reader]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--annotations", required=True, type=Path, help="JSON exported by tools/coconut_annotator.html")
    p.add_argument("--images-dir", required=True, type=Path, help="Directory containing the original images")
    p.add_argument("--reviewed-csv", required=True, type=Path, help="Human review CSV: filename,review_status,group_id,license_verified")
    p.add_argument("--provenance-csv", required=True, type=Path, help="provenance.csv from collect_commons_coconuts.py")
    p.add_argument("--output", required=True, type=Path, help="New output dataset directory; must not already exist")
    p.add_argument("--seed", default="pui89-coconut-v1", help="Fixed string seed for reproducible group assignment")
    args = p.parse_args()

    annotations_path = args.annotations.expanduser().resolve()
    images_dir = args.images_dir.expanduser().resolve()
    reviewed_path = args.reviewed_csv.expanduser().resolve()
    provenance_path = args.provenance_csv.expanduser().resolve()
    output = args.output.expanduser().resolve()
    for path in (annotations_path, reviewed_path, provenance_path):
        if not path.is_file():
            raise FileNotFoundError(f"Required file not found: {path}")
    if not images_dir.is_dir():
        raise FileNotFoundError(f"Images directory not found: {images_dir}")
    if output.exists():
        raise FileExistsError(f"Output already exists; choose a new directory to avoid overwriting: {output}")

    payload = json.loads(annotations_path.read_text(encoding="utf-8"))
    if payload.get("format") != "pui89-coconut-annotations-v1":
        raise ValueError("Unsupported annotation JSON format; export from the PUI89 offline annotator.")
    records = payload.get("images")
    if not isinstance(records, list) or not records:
        raise ValueError("Annotation JSON contains no images.")

    reviewed_rows = read_csv(reviewed_path, {"filename", "review_status", "group_id", "license_verified"})
    reviewed = {}
    for row in reviewed_rows:
        name = Path(row["filename"]).name
        if not name or name in reviewed:
            raise ValueError(f"Blank or duplicate filename in review CSV: {name!r}")
        if row["review_status"] not in {"reviewed_positive", "reviewed_negative"}:
            raise ValueError(f"{name}: review_status must be reviewed_positive or reviewed_negative.")
        if not row["group_id"]:
            raise ValueError(f"{name}: group_id is required (tree/session/source group).")
        if row["license_verified"].lower() not in {"yes", "true", "1"}:
            raise ValueError(f"{name}: license_verified must be yes after checking the original source page.")
        reviewed[name] = row

    provenance_rows = read_csv(provenance_path, {"local_file", "file_page_url", "license_short_name"})
    provenance = {}
    for row in provenance_rows:
        name = Path(row["local_file"].replace("\\", "/")).name
        if name in provenance:
            raise ValueError(f"Duplicate basename in provenance CSV: {name}")
        if not row["file_page_url"] or not row["license_short_name"]:
            raise ValueError(f"{name}: missing source page URL or licence metadata.")
        provenance[name] = row

    annotation_by_name = {}
    for item in records:
        name = Path(str(item.get("filename", ""))).name
        if not name or name in annotation_by_name:
            raise ValueError(f"Blank or duplicate filename in annotations: {name!r}")
        annotation_by_name[name] = item

    if set(annotation_by_name) != set(reviewed):
        missing_review = sorted(set(annotation_by_name) - set(reviewed))
        extra_review = sorted(set(reviewed) - set(annotation_by_name))
        raise ValueError(f"Annotation/review CSV mismatch. Missing review rows={missing_review}; extra review rows={extra_review}")
    missing_provenance = sorted(set(annotation_by_name) - set(provenance))
    if missing_provenance:
        raise ValueError(f"No provenance row for: {missing_provenance}")

    groups: dict[str, list[str]] = defaultdict(list)
    validated = {}
    for name, item in annotation_by_name.items():
        image = images_dir / name
        if not image.is_file() or image.suffix.lower() not in IMAGE_SUFFIXES:
            raise FileNotFoundError(f"Image is missing or unsupported: {image}")
        boxes = item.get("boxes", [])
        if not isinstance(boxes, list):
            raise ValueError(f"{name}: boxes must be a list.")
        status = reviewed[name]["review_status"]
        if status == "reviewed_positive" and not boxes:
            raise ValueError(f"{name}: marked positive but has no boxes.")
        if status == "reviewed_negative" and boxes:
            raise ValueError(f"{name}: marked negative but contains boxes.")
        label_lines = []
        for idx, box in enumerate(boxes, start=1):
            try:
                x, y, w, h = (float(box[k]) for k in ("x", "y", "w", "h"))
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"{name}: malformed box {idx}.") from exc
            if not all(0 <= v <= 1 for v in (x, y, w, h)) or w <= 0 or h <= 0 or x + w > 1.000001 or y + h > 1.000001:
                raise ValueError(f"{name}: box {idx} is out of bounds.")
            label_lines.append(f"0 {x + w / 2:.6f} {y + h / 2:.6f} {w:.6f} {h:.6f}")
        with image.open("rb") as _:
            pass
        group = reviewed[name]["group_id"]
        groups[group].append(name)
        validated[name] = {
            "image": image,
            "label_lines": label_lines,
            "review_status": status,
            "group_id": group,
            "provenance": provenance[name],
            "image_sha256": sha256(image),
        }

    if len(groups) < 3:
        raise ValueError(f"Need at least 3 independent group_id values to create train/val/test; found {len(groups)}.")
    # Stable hash order, then allocate whole groups to each split.
    ordered_groups = sorted(groups, key=lambda g: hashlib.sha256(f"{args.seed}|{g}".encode("utf-8")).hexdigest())
    n = len(ordered_groups)
    n_train = max(1, round(n * 0.70))
    n_val = max(1, round(n * 0.15))
    if n_train + n_val >= n:
        n_train = max(1, n - 2)
        n_val = 1
    assignments = {}
    for i, group in enumerate(ordered_groups):
        split = "train" if i < n_train else "val" if i < n_train + n_val else "test"
        assignments[group] = split

    split_counts = Counter()
    box_counts = Counter()
    manifest_rows = []
    for split in SPLITS:
        (output / "images" / split).mkdir(parents=True, exist_ok=True)
        (output / "labels" / split).mkdir(parents=True, exist_ok=True)
    for name, item in sorted(validated.items()):
        split = assignments[item["group_id"]]
        target_image = output / "images" / split / name
        target_label = output / "labels" / split / f"{Path(name).stem}.txt"
        shutil.copy2(item["image"], target_image)
        target_label.write_text(("\n".join(item["label_lines"]) + "\n") if item["label_lines"] else "", encoding="utf-8")
        split_counts[split] += 1
        box_counts[split] += len(item["label_lines"])
        source = item["provenance"]
        manifest_rows.append({
            "filename": name,
            "split": split,
            "group_id": item["group_id"],
            "review_status": item["review_status"],
            "coconut_boxes": len(item["label_lines"]),
            "image_sha256": item["image_sha256"],
            "source_page_url": source["file_page_url"],
            "license_short_name": source["license_short_name"],
            "license_url": source.get("license_url", ""),
            "creator": source.get("artist", ""),
            "credit": source.get("credit", ""),
        })

    (output / "coconut.yaml").write_text(
        "path: " + output.as_posix() + "\n"
        "train: images/train\nval: images/val\ntest: images/test\n"
        "names:\n  0: coconut\n",
        encoding="utf-8",
    )
    with (output / "dataset_manifest.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(manifest_rows[0].keys()))
        writer.writeheader()
        writer.writerows(manifest_rows)

    summary = {
        "format": "pui89-reviewed-coconut-dataset-v1",
        "status": "DATASET_BUILT_REQUIRES_FINAL_HUMAN_QA",
        "image_count": len(manifest_rows),
        "coconut_box_count": sum(box_counts.values()),
        "group_count": len(groups),
        "seed": args.seed,
        "split_image_counts": dict(split_counts),
        "split_box_counts": dict(box_counts),
        "split_group_counts": {split: sum(1 for g, s in assignments.items() if s == split) for split in SPLITS},
        "annotation_json_sha256": sha256(annotations_path),
        "review_csv_sha256": sha256(reviewed_path),
        "provenance_csv_sha256": sha256(provenance_path),
        "dataset_yaml": "coconut.yaml",
        "manifest": "dataset_manifest.csv",
        "limitations": [
            "The script does not determine whether bounding boxes are visually correct.",
            "The human reviewer must inspect every image, all visible fruit, negative examples, source page, and licence.",
            "group_id must represent a meaningful tree, capture session, video, or source group; arbitrary per-image IDs do not prevent related-image leakage.",
            "A successful build is not detector training or a performance result."
        ],
    }
    (output / "dataset_build_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print("\nNext: run training/check_dataset.py and training/audit_dataset_splits.py before training.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)

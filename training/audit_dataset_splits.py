"""Audit YOLO dataset splits for exact-image duplicates and capture-group leakage.

Optional CSV columns: split,image,group_id. The image field is relative to
images/<split>/ (or a unique basename), and group_id should identify a tree,
video, orchard session, or original source group. A group appearing in more
than one split is reported as leakage.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path, help="YOLO dataset root containing images/train, images/val, images/test")
    parser.add_argument("--groups-csv", type=Path, help="Optional CSV with columns split,image,group_id")
    parser.add_argument("--output", type=Path, default=Path("reports/dataset_split_audit.json"))
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    split_files: dict[str, list[Path]] = {}
    split_counts = {}
    missing_splits = []
    for split in ("train", "val", "test"):
        folder = root / "images" / split
        if not folder.is_dir():
            missing_splits.append(str(folder))
            split_files[split] = []
        else:
            split_files[split] = sorted(p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES)
        split_counts[split] = len(split_files[split])

    errors = []
    if missing_splits:
        errors.append("Missing split directories: " + ", ".join(missing_splits))
    if any(count == 0 for count in split_counts.values()):
        errors.append("Each train/val/test split must contain at least one image for this audit.")

    hashes: dict[str, list[dict[str, str]]] = defaultdict(list)
    basename_map: dict[str, list[dict[str, str]]] = defaultdict(list)
    for split, files in split_files.items():
        for path in files:
            rel = path.relative_to(root / "images" / split).as_posix()
            try:
                digest = sha256(path)
            except OSError as exc:
                errors.append(f"Cannot hash {path}: {exc}")
                continue
            record = {"split": split, "image": rel, "path": str(path), "sha256": digest}
            hashes[digest].append(record)
            basename_map[path.name].append(record)

    exact_duplicates = [records for records in hashes.values() if len({r["split"] for r in records}) > 1]
    duplicate_basenames = [records for records in basename_map.values() if len({r["split"] for r in records}) > 1]
    if exact_duplicates:
        errors.append(f"Found {len(exact_duplicates)} exact-image hash(es) shared across splits.")
    group_leakage = []
    groups_seen: dict[str, set[str]] = defaultdict(set)
    group_rows = 0
    if args.groups_csv:
        try:
            with args.groups_csv.expanduser().resolve().open("r", newline="", encoding="utf-8-sig") as stream:
                reader = csv.DictReader(stream)
                required = {"split", "image", "group_id"}
                if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
                    errors.append("groups CSV must contain split,image,group_id columns.")
                else:
                    for row in reader:
                        group_rows += 1
                        split = (row.get("split") or "").strip()
                        image = (row.get("image") or "").strip()
                        group_id = (row.get("group_id") or "").strip()
                        if split not in {"train", "val", "test"} or not image or not group_id:
                            errors.append(f"Invalid group manifest row {reader.line_num}.")
                            continue
                        groups_seen[group_id].add(split)
                        image_path = root / "images" / split / image
                        if not image_path.is_file():
                            # Also accept a basename only when it resolves uniquely within this split.
                            matches = [p for p in split_files[split] if p.name == image]
                            if len(matches) != 1:
                                errors.append(f"Manifest row {reader.line_num}: image not found or basename ambiguous: {split}/{image}")
                    group_leakage = [
                        {"group_id": group, "splits": sorted(splits)}
                        for group, splits in groups_seen.items() if len(splits) > 1
                    ]
                    if group_leakage:
                        errors.append(f"Found {len(group_leakage)} capture/source group(s) spanning multiple splits.")
        except OSError as exc:
            errors.append(f"Could not read groups CSV: {exc}")

    report = {
        "format": "pui89-dataset-split-audit-v1",
        "dataset_root": str(root),
        "image_counts": split_counts,
        "total_images": sum(split_counts.values()),
        "exact_duplicates_across_splits": exact_duplicates,
        "same_basename_across_splits": duplicate_basenames,
        "group_manifest": str(args.groups_csv.expanduser().resolve()) if args.groups_csv else None,
        "group_manifest_rows": group_rows,
        "groups_spanning_splits": group_leakage,
        "errors": errors,
        "ok": not errors,
        "warning": "An audit cannot prove images are representative or annotations are correct. Near-duplicates, adjacent video frames, and shared-tree leakage require source/session review."
    }
    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(output), "ok": report["ok"], "image_counts": split_counts, "exact_duplicate_groups": len(exact_duplicates), "groups_spanning_splits": len(group_leakage), "errors": errors}, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

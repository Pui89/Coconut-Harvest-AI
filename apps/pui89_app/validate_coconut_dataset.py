"""Validate a local YOLO-format coconut dataset without uploading data.

Expected layout:
    dataset/
      images/{train,val,test}/...
      labels/{train,val,test}/...

Label files use one row per object: class_id x_center y_center width height.
Coordinates must be normalized to [0, 1]. Empty label files are valid for images
with no target objects. This checks dataset structure and label syntax, not annotation
quality or model accuracy.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
SPLITS = ("train", "val", "test")


def validate_dataset(root: Path, class_count: int, splits: tuple[str, ...] = SPLITS) -> dict:
    root = root.expanduser().resolve()
    errors: list[dict[str, str]] = []
    warnings: list[str] = []
    summary: dict[str, dict[str, int]] = {}
    content_hashes: dict[str, tuple[str, str]] = {}
    if class_count < 1:
        return {
            "status": "FAIL", "dataset_root": str(root), "class_count": class_count,
            "splits": {}, "errors": [{"path": str(root), "message": "class_count must be >= 1"}],
            "warnings": [],
            "scope_note": "Structure and label syntax only; does not verify annotation correctness, split leakage, or model accuracy.",
        }

    for split in splits:
        image_dir = root / "images" / split
        label_dir = root / "labels" / split
        if not image_dir.is_dir():
            errors.append({"path": str(image_dir), "message": "Missing image directory"})
            continue
        if not label_dir.is_dir():
            errors.append({"path": str(label_dir), "message": "Missing label directory"})
            continue

        images = sorted(p for p in image_dir.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS)
        labels = sorted(label_dir.rglob("*.txt"))
        # Exact-content hashes catch copied images that would otherwise leak across splits.
        for image_path in images:
            try:
                digest = hashlib.sha256()
                with image_path.open("rb") as image_file:
                    for chunk in iter(lambda: image_file.read(1024 * 1024), b""):
                        digest.update(chunk)
                image_hash = digest.hexdigest()
            except OSError as exc:
                errors.append({"path": str(image_path), "message": f"Cannot hash image: {exc}"})
                continue
            previous = content_hashes.get(image_hash)
            if previous:
                previous_split, previous_path = previous
                if previous_split != split:
                    errors.append({
                        "path": str(image_path),
                        "message": f"Exact duplicate image content appears in split {previous_split!r}: {previous_path}",
                    })
                else:
                    warnings.append(f"Exact duplicate image content within {split!r}: {image_path} and {previous_path}")
            else:
                content_hashes[image_hash] = (split, str(image_path))
        image_by_stem: dict[str, list[Path]] = {}
        for image_path in images:
            image_by_stem.setdefault(image_path.relative_to(image_dir).with_suffix("").as_posix(), []).append(image_path)
        label_by_stem = {p.relative_to(label_dir).with_suffix("").as_posix(): p for p in labels}

        for stem, paths in image_by_stem.items():
            if len(paths) > 1:
                errors.append({"path": str(image_dir / stem), "message": "Multiple images share the same relative stem"})
        image_stems = set(image_by_stem)
        label_stems = set(label_by_stem)
        for stem in sorted(image_stems - label_stems):
            errors.append({"path": str(image_by_stem[stem][0]), "message": "Missing matching label .txt file"})
        for stem in sorted(label_stems - image_stems):
            errors.append({"path": str(label_by_stem[stem]), "message": "Label file has no matching image"})

        object_count = 0
        class_counts: Counter[int] = Counter()
        for stem in sorted(image_stems & label_stems):
            label_path = label_by_stem[stem]
            try:
                lines = label_path.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeError) as exc:
                errors.append({"path": str(label_path), "message": f"Cannot read label file: {exc}"})
                continue
            for line_number, raw in enumerate(lines, start=1):
                if not raw.strip():
                    continue
                parts = raw.split()
                if len(parts) != 5:
                    errors.append({"path": str(label_path), "message": f"Line {line_number}: expected 5 values, found {len(parts)}"})
                    continue
                try:
                    class_value = int(parts[0])
                    coords = [float(v) for v in parts[1:]]
                except ValueError:
                    errors.append({"path": str(label_path), "message": f"Line {line_number}: values must be numeric and class_id must be an integer"})
                    continue
                if class_value < 0 or class_value >= class_count:
                    errors.append({"path": str(label_path), "message": f"Line {line_number}: class_id {class_value} outside 0..{class_count - 1}"})
                    continue
                x, y, width, height = coords
                if not all(0.0 <= v <= 1.0 for v in coords):
                    errors.append({"path": str(label_path), "message": f"Line {line_number}: coordinates must be normalized to [0, 1]"})
                    continue
                if width <= 0 or height <= 0:
                    errors.append({"path": str(label_path), "message": f"Line {line_number}: box width and height must be greater than zero"})
                    continue
                if x - width / 2 < 0 or x + width / 2 > 1 or y - height / 2 < 0 or y + height / 2 > 1:
                    errors.append({"path": str(label_path), "message": f"Line {line_number}: box extends beyond image bounds"})
                    continue
                object_count += 1
                class_counts[class_value] += 1

        # Count empty label files without re-reading files that already failed to decode.
        # Keep validation reporting resilient when a label file is unreadable.
        empty_label_files = 0
        for stem in sorted(image_stems & label_stems):
            label_path = label_by_stem[stem]
            try:
                if not label_path.read_text(encoding="utf-8").strip():
                    empty_label_files += 1
            except (OSError, UnicodeError):
                # The read error was already recorded in the main validation loop.
                continue

        summary[split] = {
            "images": len(images),
            "label_files": len(labels),
            "matched_images": len(image_stems & label_stems),
            "objects": object_count,
            "empty_label_files": empty_label_files,
        }

    if not summary.get("train", {}).get("images", 0):
        warnings.append("Training split has no readable image files.")
    if not summary.get("val", {}).get("images", 0):
        warnings.append("Validation split has no image files; held-out evaluation is not yet possible.")
    if summary and all(v["objects"] == 0 for v in summary.values()):
        warnings.append("No valid objects were found in labels. Check annotation files and class mapping.")

    return {
        "status": "PASS" if not errors else "FAIL",
        "dataset_root": str(root),
        "class_count": class_count,
        "splits": summary,
        "errors": errors,
        "warnings": warnings,
        "scope_note": "Structure and label syntax only; does not verify annotation correctness, split leakage, or model accuracy.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Dataset root containing images/ and labels/")
    parser.add_argument("--classes", type=int, default=1, help="Number of classes in the dataset YAML (default: 1)")
    parser.add_argument("--splits", nargs="+", choices=SPLITS, default=list(SPLITS))
    parser.add_argument("--output", default="coconut_dataset_validation.json")
    args = parser.parse_args()
    if args.classes < 1:
        parser.error("--classes must be >= 1")

    report = validate_dataset(Path(args.root), args.classes, tuple(args.splits))
    output = Path(args.output).expanduser()
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"Saved report: {output.resolve()}")
    if report["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

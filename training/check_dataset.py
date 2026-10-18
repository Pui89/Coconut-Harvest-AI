"""Check YOLO-format coconut dataset pairs, class IDs, and normalized boxes."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from PIL import Image

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}

def check_split(root: Path, split: str) -> dict:
    image_dir = root / "images" / split
    label_dir = root / "labels" / split
    if not image_dir.is_dir() or not label_dir.is_dir():
        raise FileNotFoundError(f"Expected {image_dir} and {label_dir}")
    images = sorted(p for p in image_dir.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES)
    if not images:
        raise ValueError(f"No images found in {image_dir}")
    missing_labels, errors = [], []
    total_boxes = 0
    for image_path in images:
        rel = image_path.relative_to(image_dir)
        label_path = (label_dir / rel).with_suffix(".txt")
        if not label_path.is_file():
            missing_labels.append(str(rel))
            continue
        try:
            with Image.open(image_path) as im:
                im.verify()
        except Exception as exc:
            errors.append(f"{rel}: image unreadable ({exc})")
            continue
        for line_no, line in enumerate(label_path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            fields = line.split()
            if len(fields) != 5:
                errors.append(f"{rel}:{line_no}: expected 5 columns")
                continue
            try:
                class_id = int(fields[0])
                x, y, w, h = (float(v) for v in fields[1:])
            except ValueError:
                errors.append(f"{rel}:{line_no}: non-numeric label")
                continue
            if class_id != 0:
                errors.append(f"{rel}:{line_no}: expected single coconut class id 0, got {class_id}")
            if not all(0.0 <= v <= 1.0 for v in (x, y, w, h)) or w <= 0 or h <= 0 or x - w/2 < 0 or x + w/2 > 1 or y - h/2 < 0 or y + h/2 > 1:
                errors.append(f"{rel}:{line_no}: box coordinates must be normalized, positive, and inside image")
            total_boxes += 1
    return {
        "split": split, "images": len(images), "boxes": total_boxes,
        "missing_label_files": missing_labels, "errors": errors,
        "ok": not missing_labels and not errors,
    }

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Dataset root containing images/ and labels/.")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    results = [check_split(root, split) for split in ("train", "val", "test")]
    report = {"dataset_root": str(root), "splits": results, "ok": all(x["ok"] for x in results)}
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())

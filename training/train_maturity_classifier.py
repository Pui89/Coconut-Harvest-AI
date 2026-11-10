"""Train PUI89's small appearance classifier from an explicitly reviewed dataset."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pui89_models.coconut_maturity import CLASSES, extract_rgb_features, save_model, train

EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
REQUIRED_REVIEW_FIELDS = {
    "filename", "class_label", "review_status", "group_id",
    "license_verified", "label_qa_status", "training_approved",
}


def load_training_rows(root: Path, review_manifest: Path):
    with review_manifest.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not REQUIRED_REVIEW_FIELDS.issubset(reader.fieldnames):
            raise ValueError(f"review manifest must contain columns: {sorted(REQUIRED_REVIEW_FIELDS)}")
        records = list(reader)

    rows = []
    counts = {label: 0 for label in CLASSES}
    seen = set()
    for record in records:
        relative = Path(record["filename"])
        if relative.is_absolute() or ".." in relative.parts or len(relative.parts) != 2:
            raise ValueError(f"unsafe filename; expected class/filename: {record['filename']}")
        label, filename = relative.parts
        if label not in CLASSES or record["class_label"] != label:
            raise ValueError(f"class folder/manifest mismatch: {record['filename']}")
        if relative.as_posix() in seen:
            raise ValueError(f"duplicate manifest filename: {record['filename']}")
        seen.add(relative.as_posix())
        if (record["review_status"].strip().lower() != "reviewed"
                or record["group_id"].strip() == ""
                or record["license_verified"].strip().lower() != "yes"
                or record["label_qa_status"].strip().lower() != "passed"
                or record["training_approved"].strip().lower() != "yes"):
            raise ValueError(f"review/licence/QA/training approval gate failed: {record['filename']}")
        image_path = root / "train" / label / filename
        if not image_path.is_file() or image_path.suffix.lower() not in EXTENSIONS:
            raise ValueError(f"approved manifest image missing or unsupported: {image_path}")
        rows.append((extract_rgb_features(image_path), label))
        counts[label] += 1

    actual = {
        f"{label}/{path.name}"
        for label in CLASSES
        for path in (root / "train" / label).glob("*")
        if path.is_file() and path.suffix.lower() in EXTENSIONS
    }
    if actual != seen:
        raise ValueError(f"training folder and approved manifest differ; unlisted={sorted(actual-seen)}, missing={sorted(seen-actual)}")
    return rows, counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-root", required=True, type=Path)
    parser.add_argument("--review-manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path, help="Model JSON path outside the Git repository")
    parser.add_argument("--epochs", type=int, default=400)
    args = parser.parse_args()

    root = args.dataset_root.resolve()
    manifest = args.review_manifest.resolve()
    output = args.output.resolve()
    if not root.is_dir():
        parser.error(f"dataset root does not exist: {root}")
    if not manifest.is_file():
        parser.error(f"review manifest does not exist: {manifest}")
    if output == ROOT or ROOT in output.parents:
        parser.error("model output must be outside the Git repository; keep weights local")
    try:
        rows, counts = load_training_rows(root, manifest)
    except (OSError, ValueError) as exc:
        print(f"BLOCKED: {exc}")
        return 2
    print(json.dumps({"dataset_root": str(root), "train_class_counts": counts}, indent=2))
    if not rows:
        print("BLOCKED: no approved training images found; no model was created.")
        return 2
    missing = [label for label, count in counts.items() if count == 0]
    if missing:
        print(f"BLOCKED: every class needs reviewed training examples; missing: {missing}")
        return 2
    model = train(rows, epochs=args.epochs)
    save_model(model, output)
    print(json.dumps({
        "status": "TRAINED_EXPERIMENTAL_BASELINE",
        "output": str(output),
        "training": model["training"],
        "warning": "Uncalibrated appearance baseline; not a validated maturity or harvest decision model.",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

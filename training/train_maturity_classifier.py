"""Train PUI89's small appearance classifier from a reviewed folder dataset.

Expected layout: dataset/train/<class>/*.(jpg|png|...). Validation/test folders
are intentionally not consumed by this trainer. No downloads or installs occur.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pui89_models.coconut_maturity import CLASSES, extract_rgb_features, save_model, train

EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def load_training_rows(root: Path):
    rows = []
    counts = {}
    for label in CLASSES:
        folder = root / "train" / label
        files = sorted(p for p in folder.glob("*") if p.is_file() and p.suffix.lower() in EXTENSIONS) if folder.is_dir() else []
        counts[label] = len(files)
        for path in files:
            rows.append((extract_rgb_features(path), label))
    return rows, counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-root", required=True, type=Path)
    parser.add_argument("--output", default=Path("models/coconut-maturity-v0.1.json"), type=Path)
    parser.add_argument("--epochs", type=int, default=400)
    args = parser.parse_args()

    root = args.dataset_root.resolve()
    if not root.is_dir():
        parser.error(f"dataset root does not exist: {root}")
    rows, counts = load_training_rows(root)
    print(json.dumps({"dataset_root": str(root), "train_class_counts": counts}, indent=2))
    if not rows:
        print("BLOCKED: no training images found; no model was created.")
        return 2
    missing = [label for label, count in counts.items() if count == 0]
    if missing:
        print(f"BLOCKED: every class needs reviewed training examples; missing: {missing}")
        return 2
    model = train(rows, epochs=args.epochs)
    save_model(model, args.output)
    print(json.dumps({
        "status": "TRAINED_EXPERIMENTAL_BASELINE",
        "output": str(args.output.resolve()),
        "training": model["training"],
        "warning": "Uncalibrated appearance baseline; not a validated maturity or harvest decision model.",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

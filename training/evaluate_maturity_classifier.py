"""Evaluate a frozen PUI89 appearance model on dataset/test/<class> images."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pui89_models.coconut_maturity import CLASSES, extract_rgb_features, load_model, predict_features

EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, type=Path)
    parser.add_argument("--dataset-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if not args.model.is_file() or not args.dataset_root.is_dir():
        parser.error("model file and dataset root must exist")
    model = load_model(args.model)
    matrix = {actual: {predicted: 0 for predicted in CLASSES} for actual in CLASSES}
    abstentions = {label: 0 for label in CLASSES}
    total = 0
    for actual in CLASSES:
        folder = args.dataset_root / "test" / actual
        for image in sorted(folder.glob("*")) if folder.is_dir() else []:
            if not image.is_file() or image.suffix.lower() not in EXTENSIONS:
                continue
            result = predict_features(model, extract_rgb_features(image))
            total += 1
            if result["visual_class"] == "uncertain":
                abstentions[actual] += 1
            else:
                matrix[actual][result["visual_class"]] += 1
    if total == 0:
        print("NOT RUN: no held-out test images found.")
        return 2
    metrics = {}
    f1_values = []
    for label in CLASSES:
        tp = matrix[label][label]
        fp = sum(matrix[other][label] for other in CLASSES if other != label)
        fn = sum(matrix[label][other] for other in CLASSES if other != label) + abstentions[label]
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        metrics[label] = {"precision": precision, "recall": recall, "f1": f1, "test_count": sum(matrix[label].values()) + abstentions[label], "abstentions": abstentions[label]}
        f1_values.append(f1)
    report = {
        "status": "EXPERIMENTAL_HELD_OUT_EVALUATION",
        "model_version": model["version"],
        "test_sample_count": total,
        "confusion_matrix_excluding_abstentions": matrix,
        "per_class": metrics,
        "macro_f1_including_abstentions_as_misses": sum(f1_values) / len(f1_values),
        "abstention_count": sum(abstentions.values()),
        "abstention_rate": sum(abstentions.values()) / total,
        "limitations": ["test split must be frozen and grouped independently", "results do not establish botanical maturity or harvest readiness", "small or unrepresentative datasets require explicit warning"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

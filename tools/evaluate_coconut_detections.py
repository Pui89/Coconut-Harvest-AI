"""Evaluate coconut detector CSV predictions against manually labelled boxes.

Standard-library evaluator only; it does not run a detector or create labels.
Ground truth CSV columns: image_id,xmin,ymin,xmax,ymax,class
Predictions CSV columns: image_id,xmin,ymin,xmax,ymax,class,score
Coordinates must use the same pixel coordinate system within each image.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Box:
    image_id: str
    xmin: float
    ymin: float
    xmax: float
    ymax: float
    label: str
    score: float = 1.0


def read_boxes(path: Path, predictions: bool) -> list[Box]:
    required = {"image_id", "xmin", "ymin", "xmax", "ymax", "class"}
    if predictions:
        required.add("score")
    boxes: list[Box] = []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path}: missing columns: {', '.join(sorted(missing))}")
        for line, row in enumerate(reader, start=2):
            try:
                image_id = (row["image_id"] or "").strip()
                label = (row["class"] or "").strip()
                coords = [float(row[key]) for key in ("xmin", "ymin", "xmax", "ymax")]
                score = float(row["score"]) if predictions else 1.0
            except (TypeError, ValueError) as exc:
                raise ValueError(f"{path}: invalid numeric value or missing field on line {line}") from exc
            if not image_id or not label:
                raise ValueError(f"{path}: image_id and class must be non-empty on line {line}")
            if not all(math.isfinite(value) for value in coords + [score]):
                raise ValueError(f"{path}: values must be finite on line {line}")
            xmin, ymin, xmax, ymax = coords
            if xmin < 0 or ymin < 0 or xmax <= xmin or ymax <= ymin:
                raise ValueError(f"{path}: invalid box coordinates on line {line}")
            if predictions and not 0 <= score <= 1:
                raise ValueError(f"{path}: score must be between 0 and 1 on line {line}")
            boxes.append(Box(image_id, xmin, ymin, xmax, ymax, label, score))
    return boxes


def box_iou(a: Box, b: Box) -> float:
    ix1, iy1 = max(a.xmin, b.xmin), max(a.ymin, b.ymin)
    ix2, iy2 = min(a.xmax, b.xmax), min(a.ymax, b.ymax)
    intersection = max(0.0, ix2 - ix1) * max(0.0, iy2 - iy1)
    area_a = (a.xmax - a.xmin) * (a.ymax - a.ymin)
    area_b = (b.xmax - b.xmin) * (b.ymax - b.ymin)
    union = area_a + area_b - intersection
    return intersection / union if union > 0 else 0.0


def evaluate(
    ground_truth: list[Box],
    predictions: list[Box],
    iou_threshold: float = 0.5,
    score_threshold: float = 0.0,
) -> dict:
    if not 0 < iou_threshold <= 1:
        raise ValueError("IoU threshold must be in (0, 1].")
    if not 0 <= score_threshold <= 1:
        raise ValueError("Score threshold must be in [0, 1].")
    active = [p for p in predictions if p.score >= score_threshold]
    labels = sorted({b.label for b in ground_truth} | {b.label for b in active})
    by_class: dict[str, dict] = {}
    total_tp = total_fp = total_fn = 0
    for label in labels:
        gt_by_image: dict[str, list[Box]] = {}
        pred_by_image: dict[str, list[Box]] = {}
        for box in ground_truth:
            if box.label == label:
                gt_by_image.setdefault(box.image_id, []).append(box)
        for box in active:
            if box.label == label:
                pred_by_image.setdefault(box.image_id, []).append(box)
        tp = fp = fn = 0
        for image_id in sorted(set(gt_by_image) | set(pred_by_image)):
            truths = gt_by_image.get(image_id, [])
            preds = sorted(pred_by_image.get(image_id, []), key=lambda item: item.score, reverse=True)
            matched: set[int] = set()
            for pred in preds:
                candidates = [
                    (box_iou(pred, truth), idx)
                    for idx, truth in enumerate(truths)
                    if idx not in matched
                ]
                best_iou, best_idx = max(candidates, default=(0.0, -1))
                if best_idx >= 0 and best_iou >= iou_threshold:
                    tp += 1
                    matched.add(best_idx)
                else:
                    fp += 1
            fn += len(truths) - len(matched)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        by_class[label] = {
            "ground_truth_count": sum(len(v) for v in gt_by_image.values()),
            "prediction_count": sum(len(v) for v in pred_by_image.values()),
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "precision": round(precision, 6),
            "recall": round(recall, 6),
            "f1": round(f1, 6),
        }
        total_tp += tp
        total_fp += fp
        total_fn += fn
    precision = total_tp / (total_tp + total_fp) if total_tp + total_fp else 0.0
    recall = total_tp / (total_tp + total_fn) if total_tp + total_fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "evaluation_type": "single-threshold box detection; not average precision/mAP",
        "iou_threshold": iou_threshold,
        "score_threshold": score_threshold,
        "ground_truth_count": len(ground_truth),
        "prediction_count_after_score_threshold": len(active),
        "true_positives": total_tp,
        "false_positives": total_fp,
        "false_negatives": total_fn,
        "precision": round(precision, 6),
        "recall": round(recall, 6),
        "f1": round(f1, 6),
        "per_class": by_class,
        "limitations": [
            "This script evaluates supplied CSV boxes; it does not run a model.",
            "The result depends on annotation quality, dataset split, and score/IoU thresholds.",
            "Do not treat results on a tiny convenience sample as evidence of orchard generalization.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ground-truth", type=Path, required=True, help="CSV with manually reviewed ground-truth boxes.")
    parser.add_argument("--predictions", type=Path, required=True, help="CSV exported by a detector.")
    parser.add_argument("--iou", type=float, default=0.5, help="IoU threshold, default 0.50.")
    parser.add_argument("--score", type=float, default=0.0, help="Prediction score threshold, default 0.0.")
    parser.add_argument("--output", type=Path, help="Optional JSON output path.")
    args = parser.parse_args()
    try:
        result = evaluate(
            read_boxes(args.ground_truth, predictions=False),
            read_boxes(args.predictions, predictions=True),
            args.iou,
            args.score,
        )
    except (OSError, csv.Error, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(result, indent=2)
    print(rendered)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

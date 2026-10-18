"""Evaluate coconut bounding-box predictions against CSV ground truth.

Standard-library only. This evaluates supplied predictions; it does not run a detector.
Ground-truth CSV columns: image_file,xmin,ymin,xmax,ymax,class_name
Prediction CSV columns: image_file,xmin,ymin,xmax,ymax,class_name,confidence
Coordinates must be pixel coordinates in the same image coordinate system.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

BOX_FIELDS = ("xmin", "ymin", "xmax", "ymax")
GT_FIELDS = {"image_file", *BOX_FIELDS, "class_name"}
PRED_FIELDS = GT_FIELDS | {"confidence"}


def _read_rows(path: Path, required: set[str], predictions: bool) -> list[dict[str, Any]]:
    if not path.is_file():
        raise ValueError(f"CSV file not found: {path}")
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = sorted(required - set(reader.fieldnames or []))
        if missing:
            raise ValueError(f"{path}: missing columns: {', '.join(missing)}")
        rows: list[dict[str, Any]] = []
        for line, raw in enumerate(reader, start=2):
            image = (raw.get("image_file") or "").strip()
            class_name = (raw.get("class_name") or "").strip()
            if not image or not class_name:
                raise ValueError(f"{path}: line {line}: image_file and class_name are required")
            box: dict[str, float] = {}
            for field in BOX_FIELDS:
                try:
                    value = float(raw[field])
                except (TypeError, ValueError):
                    raise ValueError(f"{path}: line {line}: {field} must be numeric") from None
                if not math.isfinite(value):
                    raise ValueError(f"{path}: line {line}: {field} must be finite")
                box[field] = value
            if box["xmax"] <= box["xmin"] or box["ymax"] <= box["ymin"]:
                raise ValueError(f"{path}: line {line}: box must have positive width and height")
            row: dict[str, Any] = {"image_file": image, "class_name": class_name, **box}
            if predictions:
                try:
                    confidence = float(raw["confidence"])
                except (TypeError, ValueError):
                    raise ValueError(f"{path}: line {line}: confidence must be numeric") from None
                if not math.isfinite(confidence) or not 0.0 <= confidence <= 1.0:
                    raise ValueError(f"{path}: line {line}: confidence must be finite and in [0, 1]")
                row["confidence"] = confidence
            rows.append(row)
    return rows


def _iou(a: dict[str, Any], b: dict[str, Any]) -> float:
    left, top = max(a["xmin"], b["xmin"]), max(a["ymin"], b["ymin"])
    right, bottom = min(a["xmax"], b["xmax"]), min(a["ymax"], b["ymax"])
    intersection = max(0.0, right - left) * max(0.0, bottom - top)
    area_a = (a["xmax"] - a["xmin"]) * (a["ymax"] - a["ymin"])
    area_b = (b["xmax"] - b["xmin"]) * (b["ymax"] - b["ymin"])
    union = area_a + area_b - intersection
    return intersection / union if union > 0 else 0.0


def _safe_ratio(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def _evaluate_class(
    ground_truth: list[dict[str, Any]],
    predictions: list[dict[str, Any]],
    iou_threshold: float,
) -> dict[str, Any]:
    gt_by_image: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for gt in ground_truth:
        gt_by_image[gt["image_file"]].append(gt)
    matched: dict[str, set[int]] = defaultdict(set)
    ranked = sorted(predictions, key=lambda item: item["confidence"], reverse=True)
    tp_flags: list[int] = []
    fp_flags: list[int] = []

    for prediction in ranked:
        candidates = gt_by_image.get(prediction["image_file"], [])
        best_index, best_iou = -1, 0.0
        for index, gt in enumerate(candidates):
            if index in matched[prediction["image_file"]]:
                continue
            score = _iou(prediction, gt)
            if score > best_iou:
                best_index, best_iou = index, score
        if best_index >= 0 and best_iou >= iou_threshold:
            matched[prediction["image_file"]].add(best_index)
            tp_flags.append(1)
            fp_flags.append(0)
        else:
            tp_flags.append(0)
            fp_flags.append(1)

    total_gt = len(ground_truth)
    cumulative_tp = cumulative_fp = 0
    precision_points: list[float] = []
    recall_points: list[float] = []
    for tp, fp in zip(tp_flags, fp_flags):
        cumulative_tp += tp
        cumulative_fp += fp
        precision_points.append(_safe_ratio(cumulative_tp, cumulative_tp + cumulative_fp))
        recall_points.append(_safe_ratio(cumulative_tp, total_gt))

    # VOC-style all-points interpolated average precision.
    ap = 0.0
    if total_gt:
        mrec = [0.0, *recall_points, 1.0]
        mpre = [0.0, *precision_points, 0.0]
        for i in range(len(mpre) - 2, -1, -1):
            mpre[i] = max(mpre[i], mpre[i + 1])
        for i in range(1, len(mrec)):
            if mrec[i] != mrec[i - 1]:
                ap += (mrec[i] - mrec[i - 1]) * mpre[i]

    tp_total, fp_total = sum(tp_flags), sum(fp_flags)
    fn_total = max(0, total_gt - tp_total)
    precision = _safe_ratio(tp_total, tp_total + fp_total)
    recall = _safe_ratio(tp_total, total_gt)
    f1 = _safe_ratio(2 * precision * recall, precision + recall)
    return {
        "ground_truth_instances": total_gt,
        "predictions": len(predictions),
        "true_positives": tp_total,
        "false_positives": fp_total,
        "false_negatives": fn_total,
        "precision_at_confidence_ranked_predictions": precision,
        "recall": recall,
        "f1": f1,
        "ap_at_iou_threshold": ap,
    }


def evaluate(ground_truth_path: Path, predictions_path: Path, iou_threshold: float = 0.5) -> dict[str, Any]:
    if not 0.0 < iou_threshold <= 1.0:
        raise ValueError("IoU threshold must be greater than 0 and at most 1")
    gt = _read_rows(ground_truth_path, GT_FIELDS, predictions=False)
    predictions = _read_rows(predictions_path, PRED_FIELDS, predictions=True)
    if not gt:
        raise ValueError("Ground-truth CSV has no boxes; evaluation would be meaningless")

    classes = sorted({row["class_name"] for row in gt} | {row["class_name"] for row in predictions})
    per_class = {}
    for class_name in classes:
        class_gt = [row for row in gt if row["class_name"] == class_name]
        class_predictions = [row for row in predictions if row["class_name"] == class_name]
        per_class[class_name] = _evaluate_class(class_gt, class_predictions, iou_threshold)

    gt_count = sum(item["ground_truth_instances"] for item in per_class.values())
    tp = sum(item["true_positives"] for item in per_class.values())
    fp = sum(item["false_positives"] for item in per_class.values())
    fn = sum(item["false_negatives"] for item in per_class.values())
    precision = _safe_ratio(tp, tp + fp)
    recall = _safe_ratio(tp, tp + fn)
    f1 = _safe_ratio(2 * precision * recall, precision + recall)
    # Macro AP is averaged over classes present in ground truth. Predictions for
    # unknown classes remain false positives in per-class reporting but do not
    # create a new ground-truth class in the macro average.
    gt_classes = sorted({row["class_name"] for row in gt})
    macro_ap = sum(per_class[name]["ap_at_iou_threshold"] for name in gt_classes) / len(gt_classes)
    return {
        "protocol": "greedy one-to-one bounding-box matching; all-points interpolated AP",
        "iou_threshold": iou_threshold,
        "ground_truth_csv": str(ground_truth_path),
        "predictions_csv": str(predictions_path),
        "ground_truth_images": len({row["image_file"] for row in gt}),
        "prediction_images": len({row["image_file"] for row in predictions}),
        "ground_truth_instances": gt_count,
        "predictions": sum(item["predictions"] for item in per_class.values()),
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "macro_ap_at_iou_threshold": macro_ap,
        "per_class": per_class,
        "limitations": [
            "Evaluates supplied boxes only; it does not execute a detector.",
            "AP is computed at one IoU threshold, not averaged over an IoU range.",
            "Use a frozen held-out test set and record the model, weights, threshold, image preprocessing, and software versions.",
            "Bounding-box metrics do not establish ripeness, metric 3D localization, reachability, or robot safety.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ground-truth", type=Path, required=True, help="Ground-truth box CSV")
    parser.add_argument("--predictions", type=Path, required=True, help="Detector predictions CSV")
    parser.add_argument("--iou", type=float, default=0.5, help="IoU matching threshold (default: 0.5)")
    parser.add_argument("--output", type=Path, help="Optional JSON output path; defaults to stdout")
    args = parser.parse_args()
    try:
        report = evaluate(args.ground_truth, args.predictions, args.iou)
    except (OSError, ValueError, csv.Error) as exc:
        parser.error(str(exc))
    encoded = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

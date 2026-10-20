#!/usr/bin/env python3
"""Exploratory OpenCV HSV contour baseline; not a trained detector."""
import argparse
import json
import time
from pathlib import Path

import cv2
import numpy as np


def predict(path):
    image = cv2.imread(str(path))
    if image is None:
        raise ValueError(f"cannot read {path}")
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Fixed, documented heuristic: yellow/green pixels; no training or tuning.
    mask = cv2.inRange(
        hsv, np.array([15, 55, 45], dtype=np.uint8),
        np.array([48, 255, 255], dtype=np.uint8)
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    h, w = image.shape[:2]
    output = []
    for contour in contours:
        x, y, bw, bh = cv2.boundingRect(contour)
        area = bw * bh
        if area < max(900, 0.001 * w * h) or bw < 20 or bh < 20:
            continue
        if not (0.35 <= bw / max(1, bh) <= 2.8):
            continue
        output.append([x / w, y / h, (x + bw) / w, (y + bh) / h])
    return output


def iou(a, b):
    x1, y1 = max(a[0], b[0]), max(a[1], b[1])
    x2, y2 = min(a[2], b[2]), min(a[3], b[3])
    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    aa = max(0, a[2] - a[0]) * max(0, a[3] - a[1])
    bb = max(0, b[2] - b[0]) * max(0, b[3] - b[1])
    return intersection / (aa + bb - intersection) if aa + bb > intersection else 0.0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--images-dir", required=True)
    parser.add_argument("--annotations", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    annotation = json.loads(Path(args.annotations).read_text(encoding="utf-8"))
    results, runtimes = [], []
    tp = fp = fn = 0
    for item in annotation["images"]:
        ground_truth = [
            [b["x"], b["y"], b["x"] + b["w"], b["y"] + b["h"]]
            for b in item["boxes"]
        ]
        start = time.perf_counter()
        predictions = predict(Path(args.images_dir) / item["filename"])
        runtime = (time.perf_counter() - start) * 1000
        runtimes.append(runtime)
        matched = set()
        image_tp = 0
        for prediction in predictions:
            candidates = [
                (iou(prediction, target), index)
                for index, target in enumerate(ground_truth) if index not in matched
            ]
            best_iou, best_index = max(candidates, default=(0.0, -1))
            if best_iou >= 0.5:
                image_tp += 1
                matched.add(best_index)
        image_fp, image_fn = len(predictions) - image_tp, len(ground_truth) - image_tp
        tp += image_tp
        fp += image_fp
        fn += image_fn
        results.append({
            "image": item["filename"], "ground_truth_boxes": len(ground_truth),
            "predicted_boxes": len(predictions), "tp_iou50": image_tp,
            "fp_iou50": image_fp, "fn_iou50": image_fn, "runtime_ms": round(runtime, 2)
        })
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    report = {
        "benchmark_type": "exploratory_in_sample_heuristic_smoke_test",
        "method": "OpenCV HSV threshold + morphology + connected contours; no learned weights",
        "iou_threshold": 0.5, "images_evaluated": len(results),
        "ground_truth_boxes": tp + fn, "predicted_boxes": tp + fp,
        "true_positives": tp, "false_positives": fp, "false_negatives": fn,
        "precision_iou50": round(precision, 4), "recall_iou50": round(recall, 4),
        "f1_iou50": round(2 * precision * recall / (precision + recall), 4) if precision + recall else 0,
        "mean_cpu_runtime_ms_per_image": round(float(np.mean(runtimes)), 2),
        "per_image": results,
        "limitations": [
            "Only two images and 15 single-pass manually drawn boxes; independent label QA is pending.",
            "Images are not an independent held-out test set; results do not measure generalization.",
            "This is a simple non-ML reference and is sensitive to overlaps and scene colour.",
            "No trained detector, checkpoint, GPU measurement, RGB-D localization, or field performance is evaluated."
        ]
    }
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

# Fair Coconut Detector Comparison

## Purpose

`tools/compare_coconut_detectors.py` compares prediction CSV exports from multiple detectors against the same reviewed ground-truth CSV. It is dependency-free beyond the repository's Python code. It **does not run or train models**.

Use this tool to avoid comparing numbers produced with different images, labels, IoU thresholds, or confidence thresholds.

## Example

From the repository root:

```bash
python tools/compare_coconut_detectors.py \
  --ground-truth ground_truth.csv \
  --candidate hsv-baseline=hsv_predictions.csv \
  --candidate model-a=model_a_predictions.csv \
  --candidate model-b=model_b_predictions.csv \
  --iou 0.50 --score 0.25 \
  --output detector_comparison.json
```

Each prediction CSV uses the schema described in [Reproducible Detection Evaluation](REPRODUCIBLE_DETECTION_EVALUATION.md): `image_id,xmin,ymin,xmax,ymax,class,score`. The ground-truth CSV uses `image_id,xmin,ymin,xmax,ymax,class`.

## How ranking works

Candidates are sorted by F1, then recall, then precision, at the same configured thresholds. The report includes TP/FP/FN and per-class metrics. This is a transparent single-threshold ranking—not COCO AP/mAP and not an overall ranking of robot brands.

## Rules for a fair comparison

1. Freeze one rights-cleared, human-reviewed test set before model selection.
2. Use identical image IDs, ground-truth annotations, class names, IoU threshold, and score threshold.
3. Keep train/validation/test data separated by orchard, capture session, or source group where possible.
4. Tune on validation data only; use the held-out test set for final reporting.
5. Report image/object counts, class-wise metrics, failures, and confidence intervals where feasible.
6. Measure latency, peak memory, energy, installation burden, and total operating cost separately on the same hardware.
7. Do not infer maturity accuracy, 3D localization, safety, successful harvesting, or field generalization from bounding-box metrics.

## Current evidence boundary

The repository's initial HSV-contour benchmark remains precision 0 and recall 0 at IoU >= 0.50 on two images. This comparator creates no new performance result until real prediction CSVs and reviewed ground truth are supplied. Never replace missing results with synthetic examples.

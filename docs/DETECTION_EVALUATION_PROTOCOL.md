# Coconut Detection Evaluation — CSV Protocol

## Purpose and limits

`scripts/evaluate_coconut_detections.py` evaluates already-generated bounding-box predictions against human-labelled ground truth. It uses only the Python standard library. It **does not load images, run a detector, download weights, or make network requests**.

This separates model inference from metric calculation so predictions can be produced locally by whichever detector is later selected and licence-checked.

## Files

Ground truth CSV, one row per labelled coconut:

```csv
image_file,xmin,ymin,xmax,ymax,class_name
orchard_001.jpg,100,50,180,140,coconut
orchard_001.jpg,240,70,320,160,coconut
orchard_002.jpg,12,25,65,90,coconut
```

Prediction CSV, one row per model prediction:

```csv
image_file,xmin,ymin,xmax,ymax,class_name,confidence
orchard_001.jpg,101,51,179,141,coconut,0.92
orchard_001.jpg,500,200,550,260,coconut,0.34
```

- Coordinates are pixel coordinates in the same coordinate system used by the image/model preprocessing.
- Use the same image filename in both files. Keep images and labels in a frozen test split.
- Every ground-truth box must be labelled consistently. Do not silently omit difficult or occluded coconuts; define and document an uncertainty policy.
- A prediction file with no detections must still contain its header.
- CSV examples above are illustrative only, not measured observations or real benchmark results.

## Run

From the repository root, with Python 3.10 or newer:

```bash
python scripts/evaluate_coconut_detections.py --ground-truth data/annotations/test_ground_truth.csv --predictions data/predictions/test_predictions.csv --iou 0.50 --output results/test_metrics.json
```

The script reports TP, FP, FN, precision, recall, F1, per-class metrics, and all-points interpolated AP at the selected IoU threshold. It defaults to IoU 0.50. AP at a single IoU threshold is **not** COCO mAP@[.50:.95].

## Matching and interpretation

Predictions are sorted by confidence and matched greedily one-to-one to the highest-IoU unmatched ground-truth box of the same class and image. A match is a true positive if IoU meets or exceeds the configured threshold. Duplicate matches count as false positives; unmatched ground truth counts as false negatives.

The report uses macro-average AP across classes. For a single coconut class, macro AP equals that class's AP. Metrics are only as trustworthy as the annotation quality, test-set independence, and detector predictions supplied.

## Minimum reporting checklist

Record the dataset/source manifest and licence, number of test images and boxes, model name/version/weights hash, class mapping, preprocessing, confidence threshold, IoU threshold, Python and package versions, hardware, inference latency, and all exclusions. Report failures and representative examples, not only summary scores.

Detection metrics do not measure ripeness, calibrated 3D location, robot reachability, harvesting success, collision avoidance, or physical safety. Do not use this script's report as permission to operate a robot.

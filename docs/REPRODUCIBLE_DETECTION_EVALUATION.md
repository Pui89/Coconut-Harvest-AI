# Reproducible Coconut Detection Evaluation

## Purpose

tools/evaluate_coconut_detections.py evaluates bounding-box predictions exported by an existing detector against manually reviewed ground-truth boxes. It uses Python's standard library and does not download a model, call a service, or run inference.

It reports true positives (TP), false positives (FP), false negatives (FN), precision, recall, and F1 at a specified IoU and confidence threshold. It is a **single-threshold evaluation**, not average precision (AP) or mean average precision (mAP).

## CSV formats

Both CSV files use pixel coordinates in the same coordinate system for each image.

Ground truth CSV, for example ground_truth.csv:

    image_id,xmin,ymin,xmax,ymax,class
    orchard_001.jpg,12,18,83,112,coconut
    orchard_001.jpg,110,25,177,118,coconut

Prediction CSV, for example predictions.csv:

    image_id,xmin,ymin,xmax,ymax,class,score
    orchard_001.jpg,13,19,82,111,coconut,0.93
    orchard_001.jpg,220,40,260,90,coconut,0.41

Use one row per object. image_id must match between files. Coordinates must be finite, non-negative, and satisfy xmax > xmin and ymax > ymin. Prediction scores must be between 0 and 1. Include images with zero coconuts in your dataset protocol; predictions in those images count as false positives.

## Run locally

From the repository root:

    python tools/evaluate_coconut_detections.py --ground-truth ground_truth.csv --predictions predictions.csv --iou 0.50 --score 0.25 --output evaluation.json

The ground-truth and prediction CSVs above are example input filenames, not files supplied by this repository. Replace them with your own reviewed annotation and model-export files. No metrics should be reported until the files actually exist and have been checked.

## Reproducible evaluation rules

1. Freeze and document the dataset version, image source/licence, annotation instructions, and train/validation/test split before tuning.
2. Split by source image or orchard/session before creating crops or augmentations; prevent near-duplicate images from crossing splits.
3. Keep the test set separate from threshold/model selection.
4. Record the detector name/version, inference settings, class mapping, IoU threshold, and score threshold.
5. Manually audit a sample of ground-truth boxes and all unexpected false positives/false negatives where feasible.
6. Report the number of images and objects, not only precision/recall/F1. Include uncertainty and class-wise results.
7. Do not claim field generalization from a tiny convenience sample.

## Important limitations

- This tool evaluates provided box files; it does not detect coconuts or generate annotations.
- The matching procedure is greedy by descending prediction score. It is suitable for transparent single-threshold checks, not a substitute for a standardized COCO-style AP/mAP implementation.
- A valid result depends on trustworthy annotations, consistent coordinates, leakage-resistant splits, and documented thresholds.
- Detection metrics do not establish maturity classification accuracy, 3D localization, reachability, cutting safety, or robot performance.
- The repository's initial two-image baseline (precision 0 and recall 0 at IoU >= 0.50) remains unchanged by adding this evaluator. Do not replace it with illustrative or synthetic numbers.

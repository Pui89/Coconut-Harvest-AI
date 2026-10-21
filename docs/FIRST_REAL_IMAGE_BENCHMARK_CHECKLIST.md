# First Real-Image Coconut Benchmark — Operator Checklist

This is the shortest honest path from public image candidates to a reproducible, small detector evaluation. It is a manual workflow, not an automatic dataset or trained model. Do not skip rights review, human annotation, or the held-out split just to obtain a metric quickly.

## Stage 1 — Fetch candidates only when you choose

From the repository root, run:

    python scripts/prepare_real_image_review.py --download

This optional helper downloads two referenced JPEGs into `data/real_image_samples/`, records byte size and SHA-256, and creates a review CSV/source manifest. It needs internet access only for the download. It does not automatically add photos to Git or the training set.

Before using either image beyond private review, open its current source page and verify the licence, creator, attribution terms, and whether the image is suitable. If the download fails, stop and review the source page manually; do not silently substitute a different file.

## Stage 2 — Human suitability and annotation review

1. Open each downloaded photo at full resolution.
2. Record visible and occluded coconuts, lighting, clutter, and review notes in the generated CSV.
3. Reject images where individual fruit cannot be located consistently. Do not count uncertain fruit as certain labels.
4. Open `tools/coconut_annotator.html` locally and annotate only distinct, visible coconut instances. Export the annotation JSON outside Git-tracked data.
5. Run geometry checks on the exported JSON:

       python tools/audit_coconut_annotations.py --annotations path/to/coconut-annotations.json --output annotation-audit.json

6. Convert reviewed labels to YOLO format, checking that original image files exist:

       python tools/convert_annotations_to_yolo.py --annotations path/to/coconut-annotations.json --output-dir path/to/yolo-labels --images-dir data/real_image_samples

7. Inspect rendered overlays, not just the CSV or geometry report. Geometry checks cannot determine whether a box actually encloses a coconut. Record independent human QA before any training use.

## Stage 3 — Freeze split assignments before tuning

Create a CSV manifest with the columns:

    image_id,filename,split,group_id,sha256

Compute SHA-256 from each original file and record it. Use a stable group ID for the source orchard/session or original capture; all crops and near-duplicate views from one source must remain in the same split. Assign distinct source groups to train, validation, and test. Do not use the test set to select confidence thresholds or tune models.

Run the manifest audit:

    python tools/audit_dataset_split_leakage.py path/to/manifest.csv --output split-audit.json

A pass checks declared hashes and group IDs only. It does not compute the hashes, detect resized copies, verify licences, or confirm labels. Inspect findings and visually check for near-duplicates separately.

## Stage 4 — Run a real detector before calculating metrics

The evaluator requires two real CSV files. Ground truth must come from manually reviewed annotations; predictions must come from a detector actually run on the same held-out images.

Ground-truth CSV:

    image_id,xmin,ymin,xmax,ymax,class
    orchard_test_001.jpg,12,18,83,112,coconut

Prediction CSV:

    image_id,xmin,ymin,xmax,ymax,class,score
    orchard_test_001.jpg,13,19,82,111,coconut,0.93

These are format examples only, not actual labels or results. Do not copy them into a report as data. Use a detector whose weights, code version, preprocessing, inference settings, and licence are recorded. If no compatible local detector and weights are available, stop here and report that inference has not yet been run—do not invent prediction rows.

Evaluate only after the input files exist and have been checked:

    python tools/evaluate_coconut_detections.py --ground-truth path/to/ground_truth.csv --predictions path/to/predictions.csv --iou 0.50 --score 0.25 --output evaluation.json

Record the exact dataset/split, image and object counts, model/weights, code commit, hardware, software, thresholds, metrics, and failure cases. The provided evaluator reports single-threshold precision/recall/F1; it is not COCO mAP.

## Free-first and evidence rules

- No paid APIs, subscriptions, cloud GPUs, or new hardware are required by these standard-library audit/evaluation scripts.
- Optional local detector inference requires a compatible model and weights; check storage, memory, model licence, and dependencies before downloading or installing anything.
- Keep original images, labels, and model weights out of Git unless redistribution rights are explicitly confirmed.
- A successful audit or passing test is process evidence, not proof of model accuracy.
- Do not claim orchard generalization, 3D localization, cutting success, or physical robot safety from a small RGB image benchmark.
- The repository's previously reported two-image baseline (precision 0, recall 0 at IoU >= 0.50) remains the baseline until a new run is reproducibly completed. Never overwrite it with example values.

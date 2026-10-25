# Annotation Export to Benchmark Ground Truth

The offline annotator exports normalized boxes plus the image dimensions. The benchmark evaluator expects pixel-coordinate CSV rows. This converter bridges those formats without running a detector or inventing labels.

## 1. Annotate and inspect

From the repository root, open `tools/coconut_annotator.html` locally, annotate only individually distinguishable coconuts, export the JSON, and inspect every image at full resolution. Geometry checks do not establish that a box truly matches a coconut; arrange independent human label QA before benchmark use.


## Candidate 0032: preserve source metadata during manual review

For the existing candidate-0032 draft, use the local original image with basename `0032_Coconut_in_Coconut_Tree.jpg`:

1. Open `tools/coconut_annotator.html` in a local browser.
2. Select the byte-identical original image file with that exact basename.
3. Choose **Import saved JSON** and select `data/review_batch_2026-10-22/ai_annotation_draft_NOT_FOR_TRAINING.json`.
4. Review and correct every box at full resolution; remove false boxes and add only visibly identifiable missed fruit.
5. Export the JSON. The annotator preserves the imported source metadata only when the single imported draft and selected image match by filename. Exported files always set `human_qa_acknowledged: false` and `training_approved: false`; export does not assert that a review has passed.
6. If the source hash is still a placeholder, follow [Coconut Dataset Readiness](COCONUT_DATASET_READINESS.md) to run the source fingerprint check, record SHA-256 only after the fingerprint passes, and rerun the independent provenance audit.

If you annotate multiple images, or the imported source metadata does not match the selected single image, the export deliberately omits the single-source provenance object. Keep that export as an unapproved draft and reconcile its source metadata before any downstream benchmark workflow.

## 2. Validate the JSON without creating evaluator input

```powershell
python tools/annotations_to_ground_truth_csv.py --annotations path/to/coconut-annotations.json --output path/to/ground_truth.csv --images-dir data/real_image_samples
```

Without the explicit acknowledgement flag, the script validates the structure and geometry, prints a summary, and exits without writing the evaluator CSV. This is intentional.

## 3. Export after human QA

After a human has inspected the full-resolution overlays and independent label QA is complete:

```powershell
python tools/annotations_to_ground_truth_csv.py --annotations path/to/coconut-annotations.json --output path/to/ground_truth.csv --images-dir data/real_image_samples --confirm-human-qa --summary path/to/ground_truth_conversion.json
```

The flag records the operator's acknowledgement; the program cannot independently verify that review occurred. Image dimensions are taken from the annotator's JSON export. `--images-dir` checks that named image files exist, but does not re-measure their dimensions.

## 4. Run the evaluator only with actual predictions

Use a predictions CSV exported from a detector that was actually run on the same frozen held-out images:

```powershell
python tools/evaluate_coconut_detections.py --ground-truth path/to/ground_truth.csv --predictions path/to/real_detector_predictions.csv --iou 0.50 --score 0.25 --output path/to/evaluation.json
```

Do not create hand-written or illustrative prediction rows and present them as model output. If inference has not run, stop after annotation preparation and report that inference is not yet run.

## Boundaries

- The converter does not check image rights, label correctness, split independence, or test-set leakage.
- It does not run training or inference and produces no accuracy metrics.
- Keep image IDs identical in the ground-truth and prediction CSVs.
- Include reviewed images with zero visible coconuts in the evaluation protocol; predictions for those image IDs should count as false positives.
- Keep raw images and outputs out of Git when redistribution rights or data sensitivity are uncertain.

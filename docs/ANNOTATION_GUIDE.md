# Coconut Bounding-Box Annotation Guide

## Scope

This guide defines a small, consistent annotation format for evaluating coconut detection. It does not define ripeness, maturity, metric 3D position, reachability, or harvesting safety labels.

## One row per visible instance

Use `data/annotations/ground_truth_template.csv` as a starting point. Required columns:

- `image_file`: unique filename exactly matching the image used by the detector.
- `xmin,ymin,xmax,ymax`: pixel coordinates in the original image coordinate system; left/top inclusive and right/bottom exclusive is a practical convention, applied consistently.
- `class_name`: use `coconut` for the target class.

Coordinates must satisfy `xmax > xmin` and `ymax > ymin`. Keep coordinates in the same image frame as the model predictions. If the model resizes or letterboxes the image, convert predictions back to original-image coordinates before evaluation.

## Labeling rules

1. Draw a tight box around the visible coconut fruit, not the entire cluster, stem, leaf, or palm.
2. Label each distinguishable fruit as one instance. Do not create duplicate boxes for the same fruit.
3. For partly occluded fruits, box the visible fruit extent and record the occlusion in a separate metadata file if the study analyses occlusion.
4. If an object cannot be identified confidently as a coconut, flag it for adjudication instead of guessing. Define in advance whether uncertain instances are excluded, retained with an uncertainty tag, or treated as ignored; do not change this policy after seeing model results.
5. Keep a manifest containing source URL or collection ID, creator/owner, licence/permission, capture date where available, and any restrictions. Do not commit private orchard images without authorization.
6. Use stable image identifiers and group related frames from the same tree, burst, video, or capture session together when creating train/validation/test splits.

## Quality control and split discipline

- Have a second reviewer inspect a sample of labels or adjudicate disagreements where possible.
- Freeze the test set before selecting a model or threshold.
- Do not split near-duplicate video frames across training and test sets.
- Record image count, instance count, uncertain/excluded cases, and the annotation protocol version.
- Preserve the original images and a versioned copy of annotations; do not overwrite the only copy.

## Predictions

Use `data/predictions/predictions_template.csv` for model output. Include one row per predicted box and its confidence score in `[0,1]`. If no predictions exist, keep the header row and no data rows. Use the same image filenames and class names as ground truth.

## Interpretation

The evaluator measures 2D box agreement only. It does not measure fruit maturity, depth accuracy, localization in world coordinates, robot reachability, successful picking, collision avoidance, or physical safety. A small convenience sample is useful for debugging but is not sufficient evidence of generalization to worldwide orchards.

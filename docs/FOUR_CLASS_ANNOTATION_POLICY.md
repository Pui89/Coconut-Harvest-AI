# Four-Class Coconut Annotation Policy

**Status:** proposed annotation standard for human review. It is not a botanical certification standard, a trained classifier, or permission to harvest.

## Purpose

Use consistent labels for visible coconut fruit in the Coconut Harvest AI dataset. A label records the best-supported visual category for a particular intended use; it must not imply that colour alone proves physiological maturity, water content, internal quality, or harvest readiness.

## Label set

| ID | Label | Visual guidance | Annotation rule |
|---|---|---|---|
| C1 | Young green | Clearly young-looking, green fruit consistent with the project's young-coconut target | Use only when the visible evidence supports this category and the project label guide has been followed |
| C2 | Developing green | Green fruit that appears to be still developing and does not clearly meet the project's mature-green criteria | If C1 versus C2 cannot be judged reliably from the image, mark uncertain rather than guessing |
| C3 | Mature green | Green fruit judged visually consistent with mature-green harvest intent | Do not infer maturity from green colour or size alone; use contextual evidence only when it is documented and allowed by the annotation protocol |
| C4 | Brown / dry mature | Brown or aging-looking fruit consistent with the project's brown/dry-mature target | Exterior colour does not confirm internal dryness or quality; annotate only the visible appearance class |

These are **project-operational visual classes**. Cultivar, growing conditions, use case, lighting and camera colour response can change appearance. The label guide should be reviewed by a knowledgeable coconut grower or agronomist before the labels are treated as reliable maturity ground truth.

## Separate labels from scene and safety conditions

Do not create a fifth maturity class for mixed-stage bunches. Record scene conditions separately where supported, for example: mixed_stage_bunch, occluded, overlapping, backlit, blurred, damaged, or partially_visible.

Record uncertainty separately. If a fruit is too small, hidden, blurred, glare-obscured, or visually ambiguous to assign a defensible class, use the annotator's documented uncertain / needs_review outcome. Do not force it into C1–C4. If the current annotation format cannot represent uncertainty safely, leave the class unassigned and add a review note instead of inventing a class.

## Bounding-box rules

1. Draw a tight box around the **visible extent of one fruit**; do not box an entire bunch as one fruit.
2. Do not draw boxes around leaves, stems, shadows, highlights, or guessed hidden portions.
3. For overlapping fruits, draw separate boxes only when each fruit can be distinguished. Record ambiguity for inseparable overlap.
4. For a partially occluded fruit, box the visible fruit region according to the repository's annotation-tool convention and mark occlusion in the review notes. Apply the same convention consistently across all images.
5. Do not silently repair, interpolate, or copy boxes from AI-generated drafts. Treat model-suggested boxes as proposals until a human checks each box against the original image at native resolution.
6. Never resize, crop, recolour, or re-encode the source image used for provenance checks unless the dataset protocol explicitly records a derived image as a separate asset.

## Independent quality review

For every proposed training example, record separately:

- source URL, creator, licence/permission and required attribution;
- original file identity and SHA-256, calculated from the exact source bytes;
- candidate ID and filename consistency across ledgers;
- per-box geometry review and per-fruit class review;
- reviewer identity or initials, review date, and a concise note for disagreements;
- explicit training approval only after rights and annotation checks are genuinely complete.

A geometry validator can detect malformed boxes; it cannot decide whether a box encloses a coconut or whether its maturity class is correct. A provenance pass cannot approve the label. An AI-generated annotation is never independent human review.

## Disagreement and abstention

- If two reviewers disagree on class, keep the item blocked and resolve the disagreement using the documented class guide and qualified domain review.
- If the image does not support a confident class, use uncertain / needs review; do not guess.
- If the source licence or permission is unclear, keep the image out of training.
- If a fruit is not visible enough to annotate consistently, exclude it from class metrics or use a separately documented ignore-region mechanism supported by the evaluation code.
- Record class counts and exclusions after review; never fill class gaps by duplicating images or splitting near-identical frames across train and test.

## Evaluation rules

Before claiming detector or classification performance:

1. Approve examples only after rights and human QA pass.
2. Group splits by tree, orchard/source and capture session where known, so near-duplicate views cannot leak across partitions.
3. Freeze and version the test set before model selection.
4. Report per-class precision, recall and F1; include confusion counts, sample counts, confidence/abstention behaviour, and failure examples. Report mAP only when the detection evaluation protocol and annotations support it.
5. State hardware, software versions, exact command, dataset version and thresholds.
6. Mark missing results **NOT MEASURED**. Do not infer performance from synthetic tests, generic pretrained-model demos, concept images, or CI passing.

## Harvest decision boundary

The class label is not a command to cut. Any future harvest decision also needs valid geometry and reachability, obstacle/people/animal clearance, stable platform status, tool readiness, operator approval and an independent safe-stop path. Unknown or invalid inputs must lead to review or stop. No software-only checklist proves physical safety.

## Current project gate

The repository readiness snapshot dated 26 October 2026 reports 34 candidate records and **0 approved for training**. Keep that gate unchanged until actual review evidence is recorded. Start with the source and annotation review actions in [Coconut Dataset Readiness](COCONUT_DATASET_READINESS.md); candidate 0032's AI-assisted draft is explicitly not ground truth.

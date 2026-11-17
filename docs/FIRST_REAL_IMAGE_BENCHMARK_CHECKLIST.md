# First Real Coconut Image Evidence Review — Detector Disabled

**Current status:** model-based detector inference, training and evaluation are disabled in this repository. This checklist covers image-rights review, human annotation and dataset provenance only. It does not produce predictions or model-performance metrics.

## Before collecting images

1. Use only images you own or have documented permission to review and reuse.
2. Record source URL, creator, licence/permission basis, retrieval date, attribution requirements, capture session and SHA-256.
3. Keep private orchard images and weights outside the public repository.
4. Reject unreadable, irrelevant, duplicate or unsuitable images. Do not guess at hidden or ambiguous fruit.

## Human annotation

1. Open the offline annotator at `tools/coconut_annotator.html`.
2. Draw boxes only around clearly visible individual coconuts.
3. Record uncertain, occluded and partially visible fruit for review rather than inventing boundaries.
4. Export the annotation JSON outside Git-tracked data.
5. Run the geometry audit:

   ```bash
   python tools/audit_coconut_annotations.py --annotations path/to/coconut-annotations.json --output annotation-audit.json
   ```

6. Inspect rendered overlays against the original images. Geometry checks do not establish that a box actually encloses a coconut.
7. Record independent human QA and unresolved issues.

## Dataset integrity

Create a manifest with:

```csv
image_id,filename,split,group_id,sha256
```

Use a stable group ID for each tree, orchard, video or capture session. Keep related frames and near-duplicates in the same split. Record the exact dataset version and checksum. Run:

```bash
python tools/audit_dataset_split_leakage.py path/to/manifest.csv --output split-audit.json
```

A passing audit checks declared hashes and group IDs only. It does not verify licences, labels, visual quality or resized duplicates.

## Current capability boundary

- No detector framework or model checkpoint is selected.
- No image inference, detector training or model evaluation entry point is active.
- The application demo uses manually supplied example evidence and does not classify image pixels.
- No coconut precision, recall, F1, mAP, latency or orchard-generalization result is claimed.
- Dataset preparation and human annotation do not imply model readiness or robot safety.

Any future detector proposal requires separate approval, code/dependency and exact weight/data licence review, security and compatibility checks, held-out orchard data, human-reviewed labels and reproducible evaluation. Do not download models, install packages or use hosted inference without explicit approval.

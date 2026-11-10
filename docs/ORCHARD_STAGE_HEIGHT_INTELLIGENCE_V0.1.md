# Orchard Stage and Tree-Height Intelligence Engine v0.1

## What is implemented

This increment adds a standard-library-only evidence intake engine that combines two workstreams:

1. **Four-stage fruit intelligence:** validates supplied per-fruit records for `young_green`, `mature_green`, `brown_aging`, and `uncertain`; validates normalized bounding boxes; preserves source type, confidence and review status; requires human review for model predictions; keeps synthetic fixtures explicitly synthetic.
2. **Tall-palm intelligence:** maps a measured tree height into one of six planning bands from 0 to 30 m, but only when the measurement is marked `verified`, has an allowed method and has an evidence reference. Unverified, missing or invalid measurements remain `UNKNOWN`; values above 30 m remain `OUT_OF_RANGE`.

## What is not implemented

- No model reads image pixels or detects/classifies coconuts automatically.
- No height is estimated from a normal photograph, perspective or pixel dimensions.
- No depth-camera/LiDAR calibration or 3D localization is performed.
- No reachability, cutting, collection, or physical robot authorization is performed.
- A human-reviewed annotation is not automatically biological ground truth; label criteria still require knowledgeable grower/agronomist review.

The repository already contains an offline browser annotator and a YOLO conversion path. This engine is a downstream validation/reporting layer for their outputs or future model predictions, not a replacement for those tools.

## Run

From the repository root:

```bash
python -m unittest tests.test_orchard_intelligence -v
```

No dependencies, model weights, hosted API, GPU, or network access are required.

## Height bands

| Band | Height |
|---|---:|
| H1 | 0–5 m |
| H2 | >5–10 m |
| H3 | >10–15 m |
| H4 | >15–20 m |
| H5 | >20–25 m |
| H6 | >25–30 m |

Band boundaries are explicit in code and tests. Height must be a defensible measured value; the band is not a robot-reach rating. The 0–30 m range remains a research/design envelope, not demonstrated mechanical capability.

## Integration sequence

1. Human annotates individual coconuts using the existing offline annotator.
2. Label reviewers verify visual class criteria and source rights.
3. A detector, once trained and evaluated, may supply prediction records; unreviewed predictions remain review-required.
4. Tree-height measurements enter through the height metadata record with method, evidence and reviewer status.
5. The engine emits a machine-readable orchard report.
6. Existing separate harvest-assessment and safety-gate modules remain responsible for supervised eligibility; this new module never enables a cutter.

## Evidence status

Implementation status: code and unit tests added on a feature branch. CI status must be checked after PR creation. Real-image detector performance, height-estimation accuracy and physical harvesting remain unmeasured.

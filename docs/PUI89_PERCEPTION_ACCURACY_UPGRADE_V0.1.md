# Coconut Harvest AI — Perception Accuracy Upgrade v0.1

**Status:** Requirements specified; no new detector or physical harvesting capability is implemented by this document.

Shared contract: [PUI89 Perception and Accuracy Standard](https://github.com/Pui89/PUI89-Shared-AI-Core/blob/main/docs/perception/PUI89_PERCEPTION_AND_ACCURACY_STANDARD_V0.1.md).

## Priority perception tasks

1. **Individual fruit instances:** separate touching coconuts; retain per-fruit identity within a frame.
2. **Four-stage maturity:** `young_green`, `mature_green`, `yellow`, `brown_aging`; add `uncertain` as an annotation/review state, not a fifth maturity class. Do not use colour alone as biological ground truth.
3. **Cluster and bunch detection:** detect each bunch and link visible fruit instances to a cluster where evidence permits.
4. **Occlusion and visibility:** label visible, partially leaf-occluded, trunk-occluded, fruit-occluded and unknown visibility. Do not invent hidden fruit outlines.
5. **Keypoints:** fruit stem attachment, bunch stalk junction and candidate access points. A candidate cut point is a perception annotation, not a safe cutting instruction.
6. **Scene structure:** trunk, crown, fronds, leaves, ground, people, animals, tools and obstacles.
7. **Tree height:** record measured height, method, instrument/calibration, units, evidence reference and reviewer. A monocular photo or perspective estimate is not verified metric height.
8. **3D fruit position:** require calibrated depth/stereo/3D evidence, coordinate frame, uncertainty and timestamp.
9. **Reachability and collision context:** require robot geometry, calibrated pose and validated kinematics; perception alone cannot declare a harvest safe.

## Annotation rules

- Keep maturity label separate from detection box/mask quality.
- Use instance masks for overlapping fruit and leaf boundaries when practical; use boxes as the lower-cost baseline.
- Record per-label annotator, reviewer, annotation tool/version, timestamp and confidence.
- Include difficult examples: backlight, shadows, overexposure, rain, wind movement, dense canopy, distant/small fruit, unusual cultivars and partial views.
- Preserve original image files and hash them. Quarantine uncertain, duplicate, low-quality or licence-unverified files.
- Split by farm, tree and capture session; never randomly split near-identical frames across training and test.
- Keep real, synthetic and augmented data distinguishable.

## Evaluation gates

- Per-class precision, recall, F1 and declared-IoU detection results.
- Instance-mask IoU and fruit-count error where masks/counts exist.
- Keypoint pixel error for stem/attachment annotations.
- Occlusion-stratified missed-fruit and false-detection rates.
- Height absolute error only against independent measured height ground truth.
- 3D position error in metres only against calibrated reference measurements.
- Separate model accuracy from reachability, cutting, lowering, collection and full-harvest safety.

## First experiment

Start with a small, source-cleared, independently reviewed pilot. Audit labels and split leakage before training. Keep the training gate closed until provenance, reuse rights, label QA and split integrity pass. Publish counts and failure examples; use `NOT RUN` / `NOT MEASURED` for absent results.

**Safety boundary:** no perception output independently authorizes arm motion, cutting, lowering or harvesting.

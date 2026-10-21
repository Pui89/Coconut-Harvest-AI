# Coconut Harvest AI — Product Benchmark Standard

Company-wide benchmark rules: [PUI89 Product Quality and Benchmark Standard](https://github.com/Pui89/Pui89.github.io/blob/main/PRODUCT_QUALITY_AND_BENCHMARK_STANDARD.md).

## Relevant comparison set

Compare systems that perform the same job—not unrelated robot brands or generic AI models. Candidate groups to research and document:
1. Human inspection and the orchard's current recording/harvest-planning process.
2. Traditional computer-vision baseline (e.g. a clearly specified color/shape or contour method).
3. Relevant open-source object detectors/segmenters with licences checked.
4. Relevant agricultural fruit/crop detection research methods with available reproducible implementations.
5. Commercial orchard inspection or harvesting products only when public evidence and task comparability are available.

Do not imply every alternative has been tested. Maintain a dated table with source, version, licence, hardware, tested/not tested, and reason for inclusion.

## Core metrics

- Detection: precision, recall, F1 and mAP at explicitly stated IoU thresholds; per-class TP/FP/FN.
- Localization: bounding-box IoU and/or center error where applicable.
- Robustness: lighting, occlusion, distance, viewpoint, background and orchard variation.
- Workflow value: inspection/report time, human correction time, reviewed agreement, misses and false alarms.
- Runtime: end-to-end p50/p95 latency and peak memory on named existing hardware.
- Robotics: simulation-only reachability, collision, task success and recovery before any physical trial; physical cutting is a separate safety-critical milestone.

## Fair protocol

1. Create a permissioned, reviewed dataset and split it before model tuning.
2. Freeze annotations, label definitions, matching rules, confidence threshold selection method and IoU threshold.
3. Run every detector on the same held-out images and compare against the same ground truth.
4. Report class-level errors and failure examples, not only one headline score.
5. Report sample count, conditions, versions, runtime hardware and limitations.
6. Keep synthetic, development and real held-out results clearly separated.

## Current evidence warning

The repository's initial HSV-contour baseline reported precision 0 and recall 0 at IoU ≥ 0.50 on only two images. This is weak preliminary evidence, not a meaningful market ranking or proof of product performance. Do not claim superiority until a suitable held-out evaluation is complete.

## Zero-spend constraint

Use existing data only when rights and permissions are clear; use existing hardware and free/open-source software. Do not purchase datasets, APIs, compute or equipment without explicit approval. If a credible benchmark requires resources we do not have, mark it “not yet measured” rather than fabricate or incur a cost.

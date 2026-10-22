# License-First Model Strategy for Coconut Harvest AI

**Goal:** preserve a $0-cost development path while keeping future commercial deployment legally practical. This document is engineering guidance, not legal advice.

## Current decision

Use LibreYOLO with the `LibreRTDETRr18.pt` checkpoint as the first permissively licensed alternative to evaluate. Its hosted CPU smoke test completed successfully on a public bus demonstration image. That verifies the package/checkpoint can execute; it does not validate coconut detection.

- Hosted run: https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39699357117
- Smoke-test result record: [model-smoke-test-results.md](model-smoke-test-results.md)
- LibreYOLO project license: MIT for code; checkpoint licensing is separate.
- RT-DETR family documentation currently lists LibreRTDETRr18.pt code/weights as Apache-2.0. Before shipping, verify the exact Hugging Face checkpoint card, LICENSE and NOTICE files, and the version actually used.

## License rules for the project

1. **Do not assume a model's code license covers its weights.** Record both independently.
2. Keep copies/links for the exact version of each applicable LICENSE, NOTICE, model card, and source repository.
3. Review dependency licenses and any dataset/image terms before redistributing a trained model or product.
4. Record the provenance and permitted use of each image. A public image is not automatically reusable for training.
5. For a commercial release, obtain qualified legal advice if obligations are unclear.
6. Do not claim a model is “commercially cleared” until the exact artifacts and dependencies have been reviewed.

## Candidate comparison status

| Candidate | Code/weights licensing note | Smoke test | Coconut accuracy |
|---|---|---|---|
| Ultralytics YOLOv8n | Ultralytics AGPL-3.0 route; check separate commercial licensing options | Passed generic inference | Not measured |
| Ultralytics YOLO11n | Ultralytics AGPL-3.0 route; check separate commercial licensing options | Passed generic inference | Not measured |
| Ultralytics YOLO26n | Ultralytics AGPL-3.0 route; check separate commercial licensing options | Passed generic inference | Not measured |
| LibreYOLO RT-DETR R18 | LibreYOLO code MIT; RT-DETR R18 checkpoint documented as Apache-2.0; verify exact checkpoint notices before release | Passed generic inference | Not measured |

The smoke-test timings are first-prediction times on a hosted CPU and are not a fair performance ranking. Detection counts on a bus image are not accuracy metrics.

## Free, reproducible coconut benchmark plan

1. Collect a small, rights-cleared set of real coconut images, ideally from multiple trees, distances, lighting conditions and maturity states. Keep consent and source records where relevant.
2. Use the repository's local browser annotator to label visible coconuts; manually review every annotation. Do not upload private orchard images to an external service.
3. Group images by tree, capture session or orchard before splitting, so near-duplicates do not leak across train/validation/test.
4. Freeze the split and record image SHA-256, source group and annotation version. Run the existing dataset validation and split-leakage audit.
5. Fine-tune the chosen permissively licensed architecture only after checking the training implementation and checkpoint terms. Training may require a local GPU or free hosted quota; no paid service is assumed.
6. Evaluate all candidates against the same held-out ground truth. Publish precision, recall, F1, mAP@0.50, mAP@0.50:0.95, median/p95 latency after warm-up, model size, hardware, package versions and thresholds.
7. Select a production candidate only when measured coconut performance, deployment constraints, and license review all pass.

## Stop conditions

- No usable image rights/provenance: do not train on the images.
- Unclear model/checkpoint/dependency license: do not ship that artifact commercially yet.
- No held-out labelled coconut test set: do not claim accuracy or orchard readiness.
- Only generic demo inference is available: describe it as a smoke test, not a coconut detector benchmark.

## Official licensing references

- [LibreYOLO licensing overview](https://www.libreyolo.com/docs)
- [RT-DETR model and checkpoint licensing](https://www.libreyolo.com/docs/models/rt-detr)
- [LibreYOLO source repository and license caveats](https://github.com/LibreYOLO/libreyolo)
- [Ultralytics licensing](https://www.ultralytics.com/license)

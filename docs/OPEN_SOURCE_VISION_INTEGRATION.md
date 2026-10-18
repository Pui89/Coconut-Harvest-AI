# Optional DINOv2 + Anomalib vision baseline

This repository can use the PUI89 optional vision adapters for orchard inspection and harvesting research:

- [DINOv2](https://github.com/facebookresearch/dinov2) embeddings for fruit/leaf/bark visual representation and similarity experiments.
- [Anomalib](https://github.com/open-edge-platform/anomalib) anomaly scores for unusual fruit appearance, damaged equipment, or unfamiliar scenes.

These are generic features and anomaly scores, not a harvest-ready fruit detector. Train/evaluate task-specific heads on labeled orchard data and split by tree, orchard and capture day to reduce leakage. Record lighting, weather, occlusion and camera conditions. Do not infer ripeness, safety or pickability from anomaly scores alone.

## End-to-end and verification

The `pui89_vision` package provides optional adapters plus a deterministic `make_screening_record -> verify_screening_record -> human review` path. Missing evidence abstains; records always require human review and never authorize actuators. The checksum is not a digital signature. The adapter does not download weights automatically; inject explicitly loaded model objects and verify the exact model/checkpoint/dependency licenses.

Run `python -m unittest discover -s tests -v` for model-independent integrity tests. This does not establish harvesting accuracy or safe physical operation. Before hardware use, benchmark precision/recall, false detections, calibration, latency, power/memory, failure modes and person/obstacle safety in simulation and controlled trials. Keep grasping/motion behind an independent deterministic safety supervisor.

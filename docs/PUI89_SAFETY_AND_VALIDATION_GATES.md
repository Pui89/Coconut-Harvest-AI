# Safety and Validation Gates — Coconut Harvest AI

This is an AI application and agricultural robot concept. Passing Python tests does not demonstrate safe cutting, fruit capture, reachability or worker protection.

## Gate sequence
1. Data: record source/licence, hashes, annotation review, duplicates and source/tree/session-aware splits.
2. Perception: run a real detector on held-out data; report precision/recall/F1 with thresholds, counts and failure examples. A single-threshold evaluator is not mAP.
3. Geometry: test localization uncertainty, reachability and occlusion under stated assumptions.
4. Planning: test invalid targets, low confidence, stale/conflicting sensors, people/animals in the work zone and emergency stops.
5. Simulation: repeat scenarios and record collision, dropped-fruit, safe-stop and task-completion outcomes.
6. Hardware: only after independent risk assessment, guarded low-energy tests, physical emergency stop and qualified supervision. No physical validation is claimed here.

## Dataset preflight
Run: python tools/validate_coconut_dataset.py --manifest path/to/manifest.csv --annotations path/to/annotations.csv --root path/to/images --output dataset-preflight.json

Required manifest columns: image_id,path,source,license,split. Optional source_id, tree_id and session_id help detect leakage. Annotation columns: image_id,xmin,ymin,xmax,ymax,class. A preflight pass is not a model result.

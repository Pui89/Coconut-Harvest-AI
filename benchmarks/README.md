# Reproducible benchmark protocol

This folder provides a benchmark-record format and validator. It does not train a model, execute a physical robot, or establish operational performance.

## Record format

Store one JSON object per line in a versioned JSONL file such as `benchmarks/results.jsonl`. Each record must contain `scenario`, `metric`, finite numeric `value`, `unit`, `split`, integer `seed`, `source`, and `notes`.

Validate recorded results with:

```bash
python benchmarks/validate_results.py benchmarks/results.jsonl
```

Run the validator self-test with:

```bash
python benchmarks/validate_results.py --self-test
```

## Recommended metrics

- Fruit detection precision/recall or AP, with dataset and annotation protocol
- Localization error (cm), ripeness classification precision/recall
- Safe-reach proposal rate, human-review rate, false picks and missed detections
- End-to-end latency (ms), separated by lighting, occlusion, and fruit conditions

## Reproducibility and integrity

- Never insert fabricated or illustrative scores into a results file.
- Identify dataset/simulator version, split policy, hardware, software versions, sample counts, and random seeds.
- Report baselines, uncertainty/confidence intervals where appropriate, and failure cases.
- Clearly distinguish synthetic, simulated, and real-world data.
- Keep evaluation data separate from training and model selection.
- Schema validation only checks record structure; it does not validate the underlying experiment or certify safety.

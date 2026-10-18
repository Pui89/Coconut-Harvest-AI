# Open-Source Agent Plan — Coconut Harvest AI

## First implementation: deterministic planning agent

The repository now includes a small local rule-based agent at `agents/harvest_planning_agent.py`. It is deliberately the first baseline: it has no paid service, model download, API key, or extra dependency. It consumes candidate detections and positions supplied by the caller, applies transparent checks, ranks candidates, and writes an auditable JSON proposal.

This is **not** a coconut detector or a validated autonomous robot.

## Suggested development sequence

1. **Baseline (available):** rule-based target assessment and proposal output.
2. **Perception integration:** connect a separately tested detector and calibrated depth/localization module. Preserve the source and confidence of every input.
3. **Simulation:** add a robot-specific reachability and independent collision checker; keep physical execution disabled.
4. **Optional model-assisted agent:** experiment with Hugging Face `smolagents` and a locally runnable language model only after confirming the model fits available RAM/VRAM and its licence permits the intended use.
5. **Benchmark:** compare the rule-based baseline against the model-assisted version on the same fixed scenarios.

## Recommended open-source components

- [smolagents](https://github.com/huggingface/smolagents) — optional agent framework.
- [Transformers](https://github.com/huggingface/transformers) — optional model loading and inference.
- [DINOv2 Small](https://huggingface.co/facebook/dinov2-small) — visual feature extractor; not a ready-made coconut detector.
- [ROS 2 documentation](https://docs.ros.org/) — later robotics integration; use simulation first.

Do not assume that a Hugging Face model is small, free for every deployment, or open-source under an unrestricted licence. Check the model card, licence, local hardware requirements, and any dataset terms before downloading or redistributing weights. The zero-cost baseline does not require any of these optional components.

## Reproducible evaluation

Create a fixed test set containing: a high-confidence reachable candidate, a low-confidence candidate, a missing 3D position, an unknown reachability result, an occluded target, and an out-of-range target. Record:

- target-selection correctness against manually reviewed labels;
- number of incomplete/unsafe proposals rejected;
- false-rejection rate;
- run-to-run determinism;
- latency and hardware/software versions.

Do not claim a numerical performance improvement until the experiment has been executed. The provided tests validate only the prototype's rules, not real-world harvesting performance.

## Safety

The output is a proposal for simulation review only. It must not directly control a robot arm, cutter, gripper, or other actuator. Physical trials require validated sensor calibration, robot-specific reachability and collision checking, independent safety controls, emergency-stop testing, risk assessment, and supervised testing.

# Coconut Harvest Planning Agent

A zero-cost-first, local decision-support prototype for the Coconut Harvest AI repository.

## Run it

From the repository root, Python 3.10 or later is sufficient; the agent itself uses only the Python standard library.

```bash
python agents/harvest_planning_agent.py
python agents/harvest_planning_agent.py --output agent_report.json
```

To provide your own candidates, create a JSON file such as `examples/agent_candidates.example.json` and run:

```bash
python agents/harvest_planning_agent.py --input examples/agent_candidates.example.json
```

Each candidate has a `target_id`, `confidence` (0–1), optional `x_m`, `y_m`, `z_m` coordinates, a `reachable` value, and an `occluded` flag. The default policy requires a 3D position and explicitly confirmed reachability. Missing or uncertain inputs are rejected rather than guessed.

## What the prototype does

1. Applies transparent confidence, range, occlusion, and reachability checks.
2. Ranks candidates that pass those configured checks.
3. Emits a JSON proposal with reasons for rejected candidates.
4. Explicitly records that no actuator command was sent and physical execution is not authorized.

The built-in example is synthetic. This module does not run a coconut detector, estimate depth, calculate robot kinematics, or perform an independent collision check.

## Hugging Face / open-source agent path

The core version is deterministic and needs no model download, API key, subscription, or cloud service. This makes it a useful baseline.

For a later optional language-model experiment, install [smolagents](https://github.com/huggingface/smolagents) separately and connect only read-only perception summaries and bounded planning tools. Run a model locally using a compatible local inference backend if your hardware supports it. Do not give a language model direct motor, cutter, gripper, or actuator access. Check each model and dependency licence before reuse or redistribution.

A meaningful experiment is to compare this rule-based baseline with a local model-assisted agent on the same fixed test cases. Measure target-selection accuracy, rejected unsafe/incomplete proposals, tool-call failures, latency, and reproducibility. Do not report performance until you have run and recorded the experiment.

## Safety boundary

`ELIGIBLE_FOR_SIMULATION_REVIEW` means only that the supplied fields passed this prototype's configured checks. It is not a finding that a target is safe to harvest. A real robot needs calibrated sensors, validated reachability and collision checking, a robot-specific safety controller, emergency-stop tests, and supervised trials. Never connect this script directly to physical actuators.

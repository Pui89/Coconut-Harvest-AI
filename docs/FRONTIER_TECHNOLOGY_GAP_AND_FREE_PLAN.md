# Frontier technology gap and free-first adoption plan

**Review date:** 25 October 2026  
**Purpose:** identify high-value current AI/robotics techniques and adopt them without recurring bills, while keeping project claims evidence-based.

## Technology direction to adopt

- **Vision-language models (VLMs):** describe a supplied image and propose candidates; they do not replace a task-specific validated perception system.
- **Vision-language-action (VLA) and action-planning models:** a frontier direction for connecting perception and high-level actions. Start with structured plans and strict allowlists rather than downloading or running a large model.
- **World models and explicit world state:** maintain a time-stamped representation of objects, hazards, robot status, uncertainty and unknown information. This is useful even before a learned world model is available.
- **Agentic workflows:** automate repeatable code checks, dataset checks, evaluation summaries and issue triage; require explicit approval for costly installs, external services and physical actions.
- **Simulation, synthetic data and sim-to-real evaluation:** use deterministic scenarios and separate simulation results from real-world evidence.
- **Uncertainty-aware decisions:** test missing inputs, conflicting sensors, out-of-distribution examples, calibration and abstention. “Unknown” should be a valid output.
- **Edge-first engineering:** small baselines, reproducible environments, model-size checks, latency/memory measurements and no mandatory cloud dependency.

## What the repositories have now versus what is still missing

Already present in the current repository design: free software-check workflows; a software-level autonomy supervisor; model-agnostic vision/action-plan contracts; project roadmaps; and documented physical-AI architecture.

Still missing or not yet evidenced: a verified local end-to-end VLM/VLA integration; measured task-specific model accuracy; robust uncertainty calibration; completed project-specific dataset audits; reproducible navigation/multi-agent simulation metrics; and field validation. Do not describe these as completed.

## Free/no-recurring-cost implementation sequence

1. Extend standard-library tests and deterministic mock scenarios before adding packages.
2. Add local manifests, hashes, schema checks, data splits and evaluation scripts; never train on unreviewed or unlicensed data.
3. Record environment, commit, seed, inputs, outputs, failures and metrics in a reproducible report.
4. Consider a free/open-source dependency only after checking its licence, maintenance, operating-system support, install size, RAM/VRAM needs and whether it triggers any paid service.
5. Keep paid APIs, subscriptions, cloud GPU, paid storage and automatic model downloads **off by default**. Local software may still have electricity, hardware, bandwidth and maintenance costs.
6. Keep LLM/VLM outputs advisory. An independent supervisor and qualified human review remain required; software tests are not physical safety certification.

## Acceptance gate before calling a new technology “implemented”

- [ ] Code and documentation are committed.
- [ ] Tests pass in the supported environment and the run is linked.
- [ ] Dataset/model licence and provenance are documented.
- [ ] Model download size, RAM/VRAM and runtime cost have been checked before installation.
- [ ] Baseline and held-out evaluation are reported, including failure cases.
- [ ] Limitations and human-review path are explicit.

## Official technology references

- NVIDIA Isaac ROS 5.0, agentic workflows and open robotics libraries (22 September 2026): https://blogs.nvidia.com/blog/isaac-ros-5-0-agentic-open-source-robotics/
- NVIDIA Isaac Lab, open-source robot-learning simulation framework (BSD-3-Clause): https://developer.nvidia.com/isaac/lab
- Gazebo Sim, open-source physics, rendering and sensor simulation (Apache 2.0): https://gazebosim.org/libs/sim/
- Gemini Robotics ER 2, currently preview; hosted model endpoints are not assumed free: https://ai.google.dev/gemini-api/docs/robotics-overview.md
- NVIDIA Isaac Sim licensing and cloud-cost caveats: https://developer.nvidia.com/isaac/sim/

**Cost caution:** “open source” or “free to use” does not guarantee every hosted API, cloud instance, redistribution route, model weight or hardware requirement is free. This plan does not install any tools or download model weights.


## Project-specific technology priorities

1. **Small, measurable vision baseline first.** The latest README snapshot reports 34 candidate records and 0 approved for training. Resolve permissions, provenance, duplicate leakage and annotation geometry before training. Report per-maturity precision/recall/F1 and latency only from a held-out split.
2. **Open-vocabulary/VLM assistance, not replacement.** A VLM may describe a reviewed local image and suggest candidate regions; a deterministic detector/classifier and human-checked labels remain the evaluation reference. Keep live-camera operation out of scope.
3. **3D-aware target uncertainty.** Represent image box, estimated depth/range, timestamp, uncertainty and sensor source separately. Unknown depth or inconsistent estimates must block a harvest recommendation.
4. **World-state and task planning.** Track fruit identity, maturity hypothesis, occlusion, reachability estimate and tool state. Plan only high-level actions such as inspect, estimate reachability, request confirmation and verify capture; no LLM cutter/arm control.
5. **Synthetic-data and sim-to-real discipline.** Later, use simple local synthetic scenes or a free simulator to test geometry and edge cases. Keep synthetic and real-image scores separate; synthetic success does not prove orchard performance.
6. **Edge deployment gate.** Benchmark current hardware and memory before any model download. Prefer a tiny reproducible baseline and optional quantized models only after checking license, exact download size and local VRAM/RAM. No cloud GPU or paid endpoint.

## First next implementation milestone

Finish data permission/annotation review, then run a small local baseline and save raw metrics.

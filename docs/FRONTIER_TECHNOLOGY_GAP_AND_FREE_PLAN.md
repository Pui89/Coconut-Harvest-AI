# Frontier technology gap and free-first adoption plan

**Review date:** 26 October 2026  
**Purpose:** identify high-value current AI/robotics techniques and adopt them without recurring bills, while keeping project claims evidence-based.

## Technology direction to adopt

- **Vision-language models (VLMs):** describe a supplied image and propose candidates; they do not replace a task-specific validated perception system.
- **Vision-language-action (VLA) and action-planning models:** a frontier direction for connecting perception and high-level actions. Start with structured plans and strict allowlists rather than downloading or running a large model.
- **World models and explicit world state:** maintain a time-stamped representation of objects, hazards, robot status, uncertainty and unknown information. This is useful even before a learned world model is available.
- **Agentic workflows:** automate repeatable code checks, dataset checks, evaluation summaries and issue triage; require explicit approval for costly installs, external services and physical actions.
- **Simulation, synthetic data and sim-to-real evaluation:** use deterministic scenarios and separate simulation results from real-world evidence.
- **Uncertainty-aware decisions:** test missing inputs, conflicting sensors, out-of-distribution examples, calibration and abstention. “Unknown” should be a valid output.
- **Edge-first engineering:** small baselines, reproducible environments, model-size checks, latency/memory measurements and no mandatory cloud dependency.


## Technology scout update — 26 October 2026

### Current ROS 2 and Gazebo options

- **ROS 2 Lyrical Luth** was announced on 22 May 2026 as an LTS release supported until May 2031. Its Tier 1 platforms are Ubuntu 26.04 and Windows 11. See the [official ROS announcement](https://discourse.openrobotics.org/t/ros-2-lyrical-luth-released/55021).
- The current [Gazebo ROS compatibility matrix](https://gazebosim.org/docs/jetty/ros_installation/) lists **ROS 2 Lyrical + Gazebo Jetty** as a recommended pairing. However, the same page's introductory recommendation still names Ubuntu 24.04 + Jazzy + Harmonic. Treat the newer pairing as a verified candidate, not an automatic installation instruction; check the current install steps for the exact operating system and packages.
- **ROS 2 Jazzy + Gazebo Harmonic** remains a documented pairing for established Ubuntu 24.04 workflows, with Jazzy support scheduled through May 2029. Do not mix packages from different ROS/Gazebo pairings.
- **NVIDIA Isaac ROS 5.0**, announced on 22 September 2026, adds agent-ready robotics-development workflows and support for ROS 2 Lyrical. It is an optional GPU-accelerated layer, not a prerequisite for these repositories. Check the specific package's supported OS, GPU, RAM, storage, licence and dependencies before considering it. See the [official Isaac ROS 5.0 announcement](https://blogs.nvidia.com/blog/isaac-ros-5-0-agentic-open-source-robotics/).

### PUI89 adoption decision

Keep the standard-library workflow, deterministic tests, evidence reports and human-review gates as the active baseline. Do not install a robotics stack, download model weights or switch operating systems as part of this review. A simulator can be evaluated later after the host OS, free disk, RAM/VRAM and a single supported ROS/Gazebo pairing are confirmed. The immediate project-specific bottleneck remains reviewed data and measured task-specific evidence—not the newest framework.

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

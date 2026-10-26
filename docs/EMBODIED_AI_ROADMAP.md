# Free-First Embodied AI Roadmap

Reference index: [Awesome Embodied Agents](https://github.com/benchflow-ai/awesome-embodied-agents)

This roadmap is a selection guide, not a claim that every listed project is installed, integrated, or validated. Prefer small, reproducible steps that work locally and preserve a clear distinction between software tests, simulation results, and real-world evidence.

## Adoption rules

1. Inspect the current repository and reuse existing checks before adding duplicate tools.
2. Prefer free/open-source software, local execution, small dependencies, and CPU-capable smoke tests.
3. Before adopting a tool, check maintenance status, licence, dependency footprint, model/asset licences, data handling, hardware needs, and whether any hosted service incurs a cost.
4. Do not download large models or simulators automatically. Ask before any action that could create a bill, use paid APIs, or require cloud compute.
5. Every evaluation record should state the environment, scenario, software/model version, data provenance, expected outcome, observed outcome, and limitations.
6. Never interpret a simulation pass as proof of physical-robot safety or real-world performance.

## Prioritised roadmap

### P0 — Robot harnesses for coding agents

- Add repeatable commands for linting, unit tests, schema checks, and local reports.
- Keep agent permissions narrow: inspect and propose first; require explicit review before hardware control, network actions, or destructive operations.
- Record tool calls, failures, retries, and evidence links where relevant.
- Avoid a new agent framework until the existing Python and GitHub workflows show a concrete gap.

### P1 — Robot operating systems, MCP and device standards

- Treat ROS 2 as a future integration path where a project actually needs robot middleware.
- Use MCP/device interfaces only when they solve a real interoperability need; validate input schemas and permissions.
- Keep robot commands behind a mock/simulation adapter by default. Do not allow a language model to send unrestricted actuator commands.

### P2 — Reasoning models and vision-language-action models

- Begin with the current lightweight perception pipeline and deterministic task logic.
- Evaluate candidate open/local models only after checking licence, download size, VRAM/RAM, and CPU fallback.
- Measure latency, memory use, task success, uncertainty and failure cases; do not rely on a demo video as a benchmark.
- Keep model-based suggestions separate from safety-critical control.

### P3 — World models and simulation evaluators

- Start with a small set of scripted, repeatable scenarios.
- Add simulation only when a question requires physics, navigation, manipulation, or sensor interaction that unit tests cannot cover.
- Pin scenario configurations and record simulator version, seed, assets and limitations.
- Do not introduce multiple heavyweight simulators at once.

### P4 — Benchmarks, safety and benchmark integrity

- Reuse the project's evaluation helper for consistent pass/fail/blocked records.
- Include negative cases, edge cases, blocked scenarios, safety violations, and regression tests.
- Keep evaluation data separate from training data; split by source/tree/session or other leakage-relevant group, not only by random image.
- Report sample counts and uncertainty. Never invent metrics or omit failed/blocked runs from a report.

### P5 — Perception and datasets

- Track source URL, author, licence, retrieval date, hash, annotation version, reviewer, and review status for each external dataset asset.
- Run image/label geometry checks and detect duplicate or near-duplicate samples where feasible.
- Do not train on an item whose source/licence or annotation review is unresolved.
- Distinguish real measured labels from estimates, synthetic labels, and simulation assumptions.

## Project-specific application

### Coconut Harvest AI — priority 1

1. Finish image-source and licence review, annotation geometry review, and leakage-safe splits before training.
2. Add maturity-class coverage checks and separate measured palm-height labels from unverified appearance-based estimates.
3. Build a small local baseline and report precision/recall or mAP only when labels and evaluation split are ready.
4. Add task-level simulation later for reach, approach, cut, catch and post-harvest verification. The 0–30 m reach remains a design target unless independently tested.
5. Preserve the distinction between conceptual design, software prototype, simulation and validated physical harvesting.

### Extreme Flood Rescue AI — priority 2

1. Define scenario records for water depth, current, visibility, debris, communication loss, and victim state.
2. Start with scripted perception/navigation tests and safe fallback logic; label simulated conditions explicitly.
3. Treat ground robot, boat and drone as separate platforms with capability limits, not as one robot that can safely operate at every depth.
4. Add coordination and degraded-communications tests before complex multi-agent simulation.
5. Report detection, navigation, time-to-assist and safety outcomes only when a reproducible evaluator exists.

### Multimodal Narcotics Screening AI — priority 3

1. Record which sensor modalities are genuinely available; do not imply chemical detection from RGB images alone.
2. Add missing-modality, noisy-input, disagreement and low-confidence test cases.
3. Require abstention/escalation to an authorised human reviewer when evidence is uncertain or modalities conflict.
4. Evaluate false positives and false negatives per class and modality, using lawful, documented datasets.
5. Keep screening support distinct from a definitive accusation or enforcement decision.

## Tool adoption checklist

Before adding any item from the Awesome Embodied Agents list, document:

- Purpose and the project question it answers.
- Licence for code, models, datasets, robot assets and example scenes.
- Minimum supported Python/OS and local hardware requirements.
- Install size and whether weights/assets download separately.
- A minimal smoke test and expected result.
- A rollback path and any safety or privacy implications.

## Current status

This file is a roadmap only. Listing a tool or scenario does not mean it has been installed, executed, benchmarked, or validated. Keep implementation status and test evidence in separate, dated records.

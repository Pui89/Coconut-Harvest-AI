# PUI89 Autonomy Lab — phased, free-first validation

## Purpose and limits

This is a dependency-free Python scenario runner and mock Vision-Language-Action (VLA) interface. It establishes a repeatable software test baseline before optional model or robotics dependencies are considered. It does not connect to robots, run a real VLM, validate a detector, or prove physical capability.

## Phase 1 — automated checks and lightweight simulation

From the repository root, using Python 3.10 or newer:

\`\`\`powershell
python -m unittest discover -s tests -p "test_pui89_autonomy_lab.py" -v
python tools/pui89_autonomy_lab.py simulate --config simulation/scenarios.json --output-dir reports/simulation
\`\`\`

The scenario file includes nominal and adverse cases tailored to this project. The runner logs each simulated world-state snapshot, seed label, expected and actual action, guard-rule trace, simulated time, and observed step latency. It emits a JSON report with failure details plus a CSV step ledger. An action mismatch exits with status 1; invalid scenario configuration exits with status 2.

The stable run identifier is a hash of engine version and scenario configuration. Pass rates and action counts are deterministic for fixed scenarios; latency numbers and report timestamps are not. Scenario cases are static and seed labels are recorded for traceability; the current suite does not perform random sampling.

## Phase 2 — check hardware and licence before model installation

Run the offline-only preflight:

\`\`\`powershell
python tools/pui89_autonomy_lab.py preflight --probe-path . --output reports/model-readiness-preflight.json
\`\`\`

The first VLM candidate is HuggingFaceTB/SmolVLM-256M-Instruct. Its publisher model card declares Apache-2.0 and lists the main model.safetensors weight file as 513 MB. That is the main weights file, **not** the total repository size. The upstream repository also contains alternative ONNX artifacts, so avoid a full repository clone; if a download is later approved, allowlist only the required weights, config, tokenizer and processor files. Review the current model card and terms before use:

- Model card and licence: https://huggingface.co/HuggingFaceTB/SmolVLM-256M-Instruct
- Main weights file: https://huggingface.co/HuggingFaceTB/SmolVLM-256M-Instruct/blob/main/model.safetensors

The preflight samples free disk, available system RAM and NVIDIA free VRAM when available. Its resource thresholds (3 GiB free disk, 4 GiB available RAM and 1 GiB free VRAM) are screening estimates, not guarantees. Unknown hardware data is reported instead of guessed. **The command never downloads weights or installs packages.** Do not proceed just because the preflight passes: review the report and model card first.

After a local model is separately approved and installed by the operator, add a one-image smoke test with a small, rights-cleared set. Record package versions, model revision/hash, hardware, prompt, exact input hash, output, latency and peak memory. Keep outputs exploratory and compare them with human-labelled expectations. Do not claim a model was evaluated until the local smoke test has actually run.

## Phase 3 — expand only when evidence justifies it

The mock VLA returns only symbolic proposals such as SEARCH, UNKNOWN, SAFE_HOLD, REQUEST_APPROVAL, or a project-specific simulation-only action. It has no hardware adapter. Expand only after the fixed tests pass and a reviewed local VLM smoke test produces recorded evidence. Next, compare simple baseline rules and VLM-assisted proposals on a small scenario matrix, including repeated runs, stale/missing/conflicting sensors, communication loss and emergency stop. Report deterministic scenario metrics separately from host-dependent latency.

Do not connect this lab to physical actuation. Any future simulator integration should use a separately selected simulator, enforce safety gates in the simulator, and remain simulation-only until independent engineering and safety review. Passing software tests do not establish real-world reliability.

## Project-specific interpretation

- Coconut Harvest AI: HARVEST_STEP_SIMULATION_ONLY does not mean the system can identify a safe cut, reach a 30 m tree, or harvest fruit physically.
- Extreme Flood Rescue AI: water depth values including 15 m are scenario inputs only; they do not establish buoyancy, depth tolerance, or rescue performance.
- Multimodal Narcotics Screening AI: output is triage for authorized human review, never proof of chemical identity and never authorization to accuse, search, detain, seize, or enforce.

No paid API, hosted GPU, subscription, model download or package installation is required by Phase 1.

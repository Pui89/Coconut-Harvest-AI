# Frontier AI Technology and Free-First Upgrade Plan

## Goal

Advance Coconut Harvest AI through reproducible, measurable engineering improvements. Prefer free/open-source tools and local execution. Do not claim a capability is implemented until code and tests demonstrate it.

## Priority order

### P0 — Trustworthy dataset and evaluation (do first)
- Resolve outstanding image-source, license/credit, annotation-geometry and review issues.
- Keep candidate data separate from approved evaluation data.
- Split by tree/source/session where possible to reduce data leakage.
- Record dataset version, label schema, exclusions and hashes.
- Publish no precision, recall, mAP, maturity accuracy or latency claim until a reproducible evaluation produces it.

### P1 — Agentic engineering workflow (safe, deterministic first)
- Use small Python tools to inspect dataset manifests, validate annotation bounds, run tests and produce a review report.
- Treat an “agent” as a controlled workflow with explicit inputs, permitted tools, bounded outputs and a human approval step.
- Do not allow generated code or model output to promote data automatically or operate physical hardware.
- Keep optional LLM integration separate; core checks must run without an API key or network connection.

### P2 — Vision baseline and model comparison
- Establish a documented, reproducible baseline before experimenting with newer vision or vision-language models.
- Compare only on the same approved split and report metrics, runtime, hardware, model/license and limitations.
- Consider local/open-weight models only after checking memory requirements, license and compatibility with the available laptop GPU.
- Use CPU/lightweight checks by default; no paid API or cloud GPU assumed.

### P3 — Robotic task simulation and safety
- Represent detection, target selection, reachability, cutting, capture and verification as separate stages.
- Test failure cases and safe-stop behavior in simulation before any hardware integration.
- Tree-height or reach targets are design challenges, not demonstrated physical capability.

## Acceptance criteria
- Dataset promotion is blocked when required provenance, review or geometry checks fail.
- Tests cover invalid manifests, invalid boxes, missing source records and evaluation leakage checks where feasible.
- Every reported model metric is reproducible from documented commands and a fixed evaluation split.
- README distinguishes implemented, in-progress, planned and unverified capabilities.

## Free-first tool policy
Prefer Python, pytest, Ruff, GitHub Actions free usage within current limits, OpenCV and PyTorch where compatible. Check every model and dataset license before use. Do not add paid services, metered APIs or cloud compute without explicit approval.

## Current status
This document is a plan, not evidence that all listed stages are implemented or passed. Dataset blockers and model performance remain unverified until the relevant checks and evaluations are completed.

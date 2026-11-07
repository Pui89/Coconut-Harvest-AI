# PUI89 AI Agent and Hugging Face Integration Roadmap

**Project:** Coconut Harvest AI  
**Status:** Research and integration plan — not a claim that models are installed, trained, benchmarked or validated.  
**Project-specific agent scope:** Coconut bunch and maturity assessment; harvest-zone observations; worker/animal awareness; evidence-linked harvest planning. All harvesting outputs remain proposals until validated and separately authorized.

## 1. Shared PUI89 architecture

This project reuses one common agent architecture rather than creating a separate, duplicated agent framework.

1. **Perception:** turn supported sensor inputs into structured observations.
2. **Evidence and provenance:** retain source, timestamp, sensor/modality, calibration state and integrity metadata.
3. **Reasoning:** compare observations with known state and explicitly represent uncertainty and conflicts.
4. **Planning:** produce a bounded, explainable `ActionProposal` or recommendation.
5. **Coordination:** route tasks to allowlisted specialist agents; never grant unrestricted tool or code execution.
6. **Evaluation:** measure task-specific precision/recall, false positives/negatives, calibration, robustness, latency and failure cases on held-out data.

Use the canonical PUI89 contracts: `WorldState`, `Observation`, `ActionProposal` and `FailureReport`. Preserve missing, stale, noisy and conflicting evidence rather than silently filling gaps.

## 2. Hugging Face candidates

These are candidates for controlled evaluation, not approved production dependencies.

| Component | Candidate | Intended use | Current decision |
|---|---|---|---|
| Agent framework | [Hugging Face smolagents](https://github.com/huggingface/smolagents) | Structured multi-step agent orchestration and allowlisted tools | Evaluate as an optional adapter; framework, not a model |
| Vision-language | [Microsoft Florence-2-base](https://huggingface.co/microsoft/Florence-2-base) | Captioning, visual grounding and supported image tasks | First vision candidate; verify task support, model card, code and licence |
| Open-vocabulary detection | [Google OWLv2 base patch16](https://huggingface.co/google/owlv2-base-patch16) | Text-conditioned object detection | Compare with Florence-2 on project-specific labelled data |
| Robotics VLA | [Hugging Face SmolVLA](https://huggingface.co/lerobot/smolvla_base) | Research on vision-language-action in controlled simulation | Later-stage, simulation-only evaluation; no physical actuation |
| Compact language model | [Microsoft Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct) | Local instruction/reasoning experiments | Deferred until hardware and memory fit are measured |

Model availability, publisher, licence, model-card restrictions, dependency licences, weight size and required custom code must be rechecked immediately before any adoption. Do not infer that a model is free to use commercially merely because its weights are publicly downloadable.

## 3. Model registry and adoption gates

The companion `config/huggingface-model-registry.yaml` records candidates and keeps downloads disabled. Before changing a candidate to approved:

- Verify the model publisher/origin against PUI89's non-Chinese-source preference.
- Verify the exact model and dataset licences and any attribution/share-alike or use restrictions.
- Pin an immutable model revision and record the model-card URL and review date.
- Inspect repository code and dependencies; do not enable `trust_remote_code` or execute downloaded code by default.
- Record parameter count, weight size, RAM/VRAM estimate, disk requirement and CPU-only feasibility.
- Test with a small, lawful, representative fixture before considering any full dataset.
- Publish task-specific benchmark results, thresholds, sample counts, failure cases and known limitations.
- Keep model downloads, hosted inference, cloud GPUs and external endpoints disabled unless explicitly approved.

## 4. Zero-cost and safety defaults

- No paid APIs, subscriptions, metered inference, cloud GPUs or paid datasets.
- No automatic model or dataset downloads; no model weights committed to Git.
- No package installation during ordinary verification.
- Prefer optional adapters and standard-library tests so the existing project remains usable without ML packages.
- No unrestricted agent code execution, shell access, network access or secret access.
- Agents may produce evidence-linked recommendations and proposals only.
- A separate, independently tested safety controller and explicit human authorization are required before any physical action; this roadmap grants no hardware authority.
- Stop or request human review when evidence is missing, stale, conflicting, out of distribution or below the defined confidence threshold.

## 5. Implementation order

1. Reuse and test the shared PUI89 contracts, provenance and uncertainty handling.
2. Add a model-registry reader and validation tests without downloading weights.
3. Define this project's labelled benchmark fixtures and evaluation protocol.
4. Compare Florence-2 and OWLv2 only on supported tasks and report results separately.
5. Add a smolagents adapter only after tool allowlists, budgets, audit logs and failure handling are tested.
6. Consider SmolVLA only in a versioned simulator after a separate robotics safety review.
7. Approve any model for a real workflow only after licence, hardware, security and benchmark gates pass.

## 6. Evidence status

At the time this roadmap is added, model integration is **proposed / not yet measured**. No claim is made that any listed model has been downloaded, run, fine-tuned, benchmarked or validated in this repository. A model name in the registry is not evidence of capability.

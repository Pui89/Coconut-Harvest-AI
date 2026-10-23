# Free-first local AI tooling

This guide records optional local tooling for PUI89 development. It does not claim that any software is installed on a developer's computer.

## Recommended order

1. Keep Python unit tests, dataset validation, and GitHub Actions as the source of truth for deterministic checks.
2. Optionally install [Ollama](https://ollama.com/download) to experiment with a small local language model for documentation and coding assistance.
3. Consider [n8n Community Edition](https://docs.n8n.io/hosting/) only if a real multi-step workflow is needed. Self-hosting still has setup and maintenance costs.
4. Do not add an AI agent to dataset approval, safety decisions, cutting control, or deployment gates. Those gates must remain deterministic and require human approval where specified.

## Ollama on Windows

Official instructions: https://docs.ollama.com/windows

Before installing, check free disk space and available RAM. Ollama itself requires disk space, and model files take additional space; some models are several gigabytes. This project laptop has previously been reported with 4 GB GPU VRAM, so start with a small model and stop if memory pressure becomes high. Do not download a large model by default.

After installation, open a new terminal and verify:

```powershell
ollama --version
ollama list
```

Only after reviewing the model size and license, download a suitable small model from the official library. Model use is optional; this project does not depend on Ollama to run tests.

## Safety and evidence rules

- Do not send private datasets, credentials, access tokens, or sensitive records to external services.
- Treat model-generated code and annotations as suggestions, not verified facts.
- Never let an LLM approve image rights, ground-truth annotations, dataset promotion, physical robot motion, or cutting actions.
- Record exact commands, versions, hardware, and test results before claiming an experiment succeeded.
- No paid APIs, subscriptions, cloud GPU, or metered service is required by this guide.
- Installation has not been performed by this document; a developer must install software locally and verify it.

## Project-specific use

- **Coconut Harvest AI:** documentation assistance only until dataset rights, annotations, independent QA, and leakage-safe splits pass the promotion gate.
- **Flood Rescue AI:** optional help writing simulation scenarios; navigation and safety checks remain deterministic and test-driven.
- **Multimodal Narcotics Screening AI:** optional help documenting workflows; no model may assert chemical identity or replace mandatory human review.

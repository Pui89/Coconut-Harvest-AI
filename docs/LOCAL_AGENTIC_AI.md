# Local Agentic AI Options — Coconut Harvest AI

1. Start with the existing standard-library `agents/project_agent.py`, typed proposal contracts in `pui89_autonomy/llm_interfaces.py`, and the deterministic safety supervisor. These remain the default path and run without a hosted LLM.

2. If local-language-model reasoning is demonstrably useful, evaluate Ollama with an already downloaded, licence-reviewed small model; do not run `ollama pull` automatically. Model files may be several gigabytes and each model has separate terms.

3. For explicit multi-step state and review routing, evaluate LangGraph locally. For a small tool-using agent, evaluate smolagents with a fixed allowlist and no unrestricted code executor. PydanticAI is an alternative if typed output schemas and agent evaluation are the main requirement.

4. Only consider an LLM when the deterministic baseline is insufficient. Compare it with the baseline on the same coconut images and report mistakes, unknowns, latency, memory and per-maturity performance.

## Free/open-source agent options

| Resource | What it contributes | Licence / cost boundary | Local availability check |
|---|---|---|---|
| [smolagents](https://github.com/huggingface/smolagents) | Small tool-using agent framework; supports local Transformers/Ollama model paths. | Apache-2.0 library. A hosted model, tool, sandbox or external service may introduce separate costs. Code-executing agents are high risk; use only the minimal tool-calling path. | Python module \`smolagents\` |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Explicit, stateful agent/workflow graphs, branching, retries and review checkpoints. | MIT-licensed library. Keep orchestration local; hosted observability/deployment products are optional and are not part of this plan. | Python module \`langgraph\` |
| [PydanticAI](https://github.com/pydantic/pydantic-ai) | Typed agent I/O, validation-friendly interfaces and test/evaluation helpers. | MIT-licensed library. Provider choice determines whether inference is local or billed. Built-in test models are for workflow tests, not real inference. | Python module \`pydantic_ai\` |
| [Ollama](https://github.com/ollama/ollama) | Local model runtime on a supported desktop. | MIT-licensed runtime; each downloaded model has its own licence and size. Do not use hosted providers or pull weights without an explicit resource/licence check. | Executable \`ollama\` |
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | Local inference runtime for supported GGUF models; useful as an alternative to Ollama. | MIT-licensed runtime; model weights and bundled components retain their own terms. Building from source can require disk and build tools. | Executable \`llama-cli\` or \`llama-server\` |

The probe checks only whether a local Python module or executable appears to exist; it does **not** download anything, launch a server, inspect model weights or verify model licences. Both frameworks and runtimes are optional.

## Recommended implementation pattern

Use the existing project-specific rule-based agent as the baseline. If the workload later justifies it, place a local agent framework around this controlled pipeline:

\`\`\`text
read-only evidence tools
    -> specialist proposal(s)
    -> typed schema / provenance validation
    -> deterministic project safety supervisor
    -> human review or UNKNOWN / SAFE_HOLD
    -> reproducible report
\`\`\`

Keep the following boundaries:
- No paid API keys, cloud inference, hosted agents or network-search tools are required by this design.
- No automatic \`pip install\`, model pull, model download, container build or server startup.
- Only explicitly allowlisted, read-only tools; no general shell, arbitrary Python execution, filesystem mutation or self-modifying agent.
- Enforce bounded tool calls/retries, explicit timeouts, schema validation and auditable input references.
- Treat LLM output as untrusted proposals. The deterministic supervisor outranks every agent.
- Never let an agent publish motor, cutter, propulsion, navigation, flight, boat, screening-enforcement or other actuator commands.
- Capture model ID/version/licence, prompt/config revision, evidence hashes, latency, resource use, failures and reviewer outcome when an actual model test is later run.

## Cost-safe adoption gates

1. **Now:** use the existing standard-library agent and unit tests; no framework installation needed.
2. **Later:** run the optional-resource checker. Compare the current deterministic baseline first and verify free disk, RAM and GPU memory.
3. **Choose one framework, not all three.** Try LangGraph when explicit graph/state behaviour is needed; try smolagents for a small allowlisted tool loop; try PydanticAI for strict typed interfaces and evaluation.
4. **Choose one local inference runtime at most initially** (Ollama *or* llama.cpp), then manually review the exact model licence and download size before acquiring weights.
5. **Keep model inference optional in CI.** Use deterministic fake/test models for unit tests; do not require model weights or network access for core tests.

No framework or runtime is installed by this documentation change. Software licences do not waive the separate terms of model weights, datasets, plugins, or dependent tools.

## Project-specific agent roles

- **Dataset steward:** Verify source, licence, SHA-256, annotation review and leakage-safe splits; never approve missing provenance.
- **Vision evaluator:** Summarize supplied detector metrics and image-quality flags; never invent detection results.
- **Harvestability assessor:** Return NEED_DATA/UNKNOWN where maturity, fruit location, reachability, obstacle clearance or sensor health is not established.
- **Plan proposer:** Propose a high-level harvest step for review; never publish motor, cutter or arm commands.
- **Safety and evidence supervisor:** Enforce preconditions, human approval and immutable experiment references before any future hardware interface is considered.

## Safety boundary

An AI proposal is not permission to pick a fruit. Target maturity, cutting position, reachable height (including the 0–30 m concept target), obstacle clearance and all hardware capability claims require independent evidence. The agent must not turn the conceptual reach target into a capability claim.

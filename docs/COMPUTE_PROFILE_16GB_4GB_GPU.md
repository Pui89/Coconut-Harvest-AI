# Compute Profile: 16 GB RAM and 4 GB Laptop GPU

This profile is tailored to a Windows x64 laptop with an Intel Core i7-11800H, 16 GB system RAM, an NVIDIA RTX 3050 Laptop GPU with 4 GB VRAM, and approximately 299 GB free disk space at the time the hardware details were supplied.

This is a planning guide, not a claim that the recommended configuration has been installed or tested on that device.

## Recommended operating mode

**Default: CPU-first development; optional small-model GPU inference after a preflight check.**

The CPU is suitable for repository tests, CSV evaluation, image-manifest hashing, split-leakage checks, and lightweight data review. The 4 GB VRAM limit is the main constraint for deep-learning workloads. A GPU being present does not guarantee that a model, framework, image batch, and all intermediate tensors will fit.

| Workload | Recommendation | Why |
|---|---|---|
| Python unit tests and code quality checks | Run first on CPU | Low memory requirement; gives reproducible software evidence |
| CSV detector evaluation and dataset audits | Run on CPU | These tools do not require a GPU |
| Human annotation and image review | Use small batches | Preserves system memory and makes quality review manageable |
| Inference using already-available small detector weights | Optional, after preflight | Actual VRAM use depends on architecture, framework, image size, batch size and precision |
| Training or fine-tuning | Defer until a specific model and dataset are assessed | 4 GB VRAM can be restrictive; training needs more memory than simple inference |
| Large vision-language models or multi-billion-parameter models | Do not download as the next step | Likely to consume substantial RAM/VRAM and disk, and may not fit comfortably |
| ROS/Gazebo simulation | Start with a minimal scene and one process at a time | Simulation can be CPU- and memory-intensive independently of AI model size |

## Safe preflight checklist

Before installing a deep-learning framework or downloading weights:

1. Open Task Manager and check available RAM, GPU dedicated memory, and disk space while other applications are closed.
2. Check whether NVIDIA drivers are working. If the `nvidia-smi` command is available, record its output; do not install or update drivers solely because this guide mentions it.
3. Record the Python version and current project environment.
4. Run the lightweight repository tests first: `python -m unittest discover -s tests -v`
5. Select one candidate model only after checking its size, framework requirements, input resolution, licence, and whether pretrained weights can legally be used for the intended purpose.
6. Begin inference with one image at a time and a modest input resolution. Reduce resolution or use CPU if memory errors occur. Do not interpret this as a fair performance comparison unless the evaluation protocol fixes the settings.
7. Keep the actual command, model/weights identifier or checksum, environment, image split, output file, and any error message in the experiment record.

## Evidence we can generate without GPU inference

These tasks can strengthen engineering evidence without pretending to establish AI accuracy:

- Run unit tests for the evaluator and dataset-audit tools.
- Verify image manifest hashes against local files.
- Audit source groups and split leakage.
- Human-review a small rights-cleared image sample and record annotation disagreements.
- Test the detector-evaluation code with clearly labelled synthetic test fixtures, keeping those fixtures separate from real benchmark results.
- Create a run report that explicitly marks model inference as **not run** until genuine predictions exist.

## Non-negotiable evidence rules

- Never substitute synthetic/example predictions for real model output.
- Never describe a software test as proof of coconut-detection accuracy or safe physical harvesting.
- Report precision, recall, F1, and the IoU threshold only for the exact reviewed ground truth and genuine predictions used. The repository's current CSV evaluator is not an mAP evaluator.
- Do not claim a speed, energy, memory, or robotics advantage without measuring it under a documented protocol.
- No paid cloud compute, paid APIs, or subscription services without explicit approval.
- Do not commit private images, unlicensed datasets, model weights, API keys, or device identifiers.

## Current scope

The laptop specifications support a sensible CPU-first workflow and may support selected small-model experiments. They do **not** establish that any particular detector will fit, run correctly, or achieve useful accuracy. Confirm this with a controlled preflight and real inference before making those claims.

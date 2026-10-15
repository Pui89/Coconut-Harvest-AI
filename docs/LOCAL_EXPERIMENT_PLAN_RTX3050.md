# Local experiment plan for the RTX 3050 laptop

## Known hardware

These values were supplied by the project owner and have not been independently measured by this repository:

- Windows 64-bit laptop
- Intel Core i7-11800H
- NVIDIA GeForce RTX 3050 Laptop GPU, **4 GB dedicated VRAM**
- **16 GB system RAM**
- Python 3.14.5
- Approximately 294 GB free storage, based on the supplied Windows storage figures

The GPU memory is the key constraint for model inference. Start with batch size 1 and small images; do not try to load several vision models at once.

## First step: read-only environment check

From the repository root, run:

~~~powershell
python scripts/check_local_environment.py
~~~

The script only reads local environment information. It does not install packages, download models, contact a server, alter settings, or issue robot commands. Save or copy its output when asking for help.

## Python compatibility

Keep the existing Python 3.14.5 installation. Do not uninstall it. Before installing the AI stack, check whether the currently available Windows PyTorch build and all required project dependencies support that Python version. If they do not, use a separate Python 3.12 environment alongside Python 3.14.5; this does not require replacing the existing installation.

Do not run a bulk dependency upgrade as the first step. Resolve installation compatibility in a virtual environment so the system Python stays unchanged.

## Hardware-aware experiment sequence

### Stage 0 — Verify the current prototype (no model download)

1. Create and activate an isolated environment using a supported Python version.
2. Install the project and development dependencies only after confirming compatible package builds.
3. Run the existing synthetic demo and tests:
   ~~~powershell
   python demo_end_to_end.py
   python -m pytest
   ~~~
4. Record Python/PyTorch versions, test results, elapsed time, report status, and whether CUDA is available.
5. Confirm the report says **actuator_commands_sent: false** and **trajectory_is_verified: false**.

This stage tests the software workflow, not coconut detection. Synthetic images and manually supplied evidence are not ground-truth model predictions.

### Stage 1 — Small, local vision experiment

Candidate model: **microsoft/Florence-2-base**, subject to reviewing its model card, licence and code before installation.

- Download weights only after the owner explicitly chooses to proceed; first download uses internet data and local disk.
- Use one image per inference and a small input resolution to start.
- Close other GPU-heavy applications.
- Never use paid hosted inference, cloud GPUs, paid notebooks or an automatic hosted endpoint.
- If VRAM is insufficient, stop and reduce the workload or use CPU inference; do not create a cloud resource to work around it.
- Keep this experiment separate from the safety-gated robot pipeline until outputs and failure cases have been reviewed.

Florence-2-base is a general vision-language model, not a validated coconut detector. Grounding or captioning results alone do not establish coconut detection accuracy, ripeness, 3D position, or harvestability.

### Stage 2 — Evidence suitable for a research case study

1. Assemble a permitted, representative set of orchard images.
2. Label coconut bounding boxes consistently; record image source and licence.
3. Split data by source/tree/session where possible to reduce near-duplicate leakage.
4. Establish a simple baseline before fine-tuning.
5. Report precision, recall, F1 and mAP using a documented evaluation script and held-out labels.
6. Report inference latency, input size, device, peak VRAM if measurable, and failure cases.
7. Include limitations and do not report unmeasured numbers.

Do not claim success from synthetic images or training-set results alone. No dataset or performance metric is implied to exist until it is actually collected and measured.

### Stage 3 — Robotics simulation

Use the existing safety-gated software prototype first. Before any physical hardware work, the project needs a validated robot model, calibrated sensor inputs, an independent collision checker, appropriate physics validation, emergency-stop testing and a documented risk review. The current planner is not proof of collision-free motion.

## Explicit cost boundary

- No paid APIs, cloud GPUs, paid notebooks, subscriptions or cloud-billing setup.
- No Roboflow or automatic uploads of private orchard images.
- No automatic model-weight downloads in CI.
- Model downloads use internet data and disk space; local computation uses electricity.
- Check model, dataset and dependency licences before redistribution.
- Stop if any setup page requests billing details or proposes a paid service.

## Status

This document is an experiment plan, not evidence that the model has been downloaded, integrated, tested on the owner's laptop, or validated in an orchard.

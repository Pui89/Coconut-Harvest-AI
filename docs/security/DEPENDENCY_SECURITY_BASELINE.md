# Dependency security baseline

This file records minimum dependency floors for the current Python application baseline. It is not a generated lockfile and does not claim that a resolved environment has been installed or tested.

## Required runtime baseline

- Python: 3.11 or newer.
- PyTorch: 2.15.0 or newer. The PyTorch advisory GHSA-v32g-mr63-3j83 affects versions from 2.14.0 and identifies 2.15.0 as patched. PyTorch 2.15 drops Python 3.10 wheel support, so the project metadata and installation guidance require Python 3.11+.
- Transformers: 5.10.1 or newer. This avoids the affected range through 5.8.1 in GHSA-x9r9-c232-4q39 and is above the 5.10.0 patch threshold in GHSA-xrqw-3rrv-vx5w. Version 5.10.0 was yanked on PyPI; do not select it.

## Model and checkpoint handling

- Do not load checkpoints from untrusted or unreviewed sources.
- Keep `trust_remote_code=False` unless a model's code has been independently reviewed and explicit approval is given.
- Prefer `safetensors` where the model supports it, and record immutable model revisions for experiments.
- The PyTorch advisory demonstrates that `weights_only=True` alone does not mitigate the specific affected 2.14.x checkpoint file-read issue.

## Reproducibility and validation status

- Dependency floors are recorded in `pyproject.toml` and the repository requirements entry point.
- A complete platform-specific lockfile is intentionally deferred until dependency resolution is performed in a controlled Python 3.11+ CPU environment. CPU and accelerator wheel selections can differ.
- This change does not install packages, download model files, run model inference, or certify runtime compatibility. The normal PR checks must pass, followed by an explicitly approved local CPU-only dependency validation.

## Primary advisories

- https://github.com/advisories/GHSA-v32g-mr63-3j83
- https://github.com/advisories/GHSA-x9r9-c232-4q39
- https://github.com/advisories/GHSA-xrqw-3rrv-vx5w
- https://pytorch.org/blog/pytorch-2-15-release-blog/

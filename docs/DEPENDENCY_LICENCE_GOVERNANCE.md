# Dependency licence governance

## Purpose

PUI89 screens the installed Python dependency set for missing, unknown, and
proprietary licence metadata, and blocks NVIDIA NVSHMEM packages from the
default application environment. This is a risk-screening control, not a
legal opinion or a declaration that every component is approved for
commercial distribution.

## NVIDIA NVSHMEM alert

The Aikido finding identified `nvidia-nvshmem-cu13` in the dependency
environment, although it was not directly declared in the checked-in
requirements files. It may be introduced transitively by a GPU-enabled
PyTorch/CUDA installation. The project does not need a GPU-cluster
communication runtime for its default CPU-first checks, so this package is
blocked by the new metadata audit.

The upstream NVSHMEM source repository has published Apache-2.0 licensing
information, but that alone does not establish the complete licence and
redistribution terms for every PyPI wheel or bundled component. Do not
treat the Aikido alert as resolved solely from the upstream repository
licence.

## CPU-first audit

The GitHub Actions workflow installs the CPU-only PyTorch wheel before
installing the project's declared Python dependencies. It then inventories
the installed packages and fails if it detects:
- NVIDIA NVSHMEM packages in the default environment;
- missing or unknown package licence metadata; or
- package metadata explicitly indicating a proprietary/commercial licence.

The workflow uploads a JSON inventory even when the policy check fails.
A failure is intentional: review the package, its exact version, the
upstream licence text, wheel contents, and redistribution obligations before
adding a documented exception. Do not silence a finding just to obtain a
green badge.

## Important scope limits

A passing metadata check does **not** establish that:
- all package licences permit every intended commercial use;
- model weights, checkpoints, datasets, images, fonts, or other assets are
  commercially usable;
- copyright notices and attribution obligations have been fulfilled;
- the application has been legally cleared for sale or distribution.

Those assets require their own provenance and licence review. Keep
verified facts separate from proposals in project documentation.

## Local use (optional)

The audit script accepts a JSON report created by `pip-licenses`:

```bash
pip-licenses --format=json > dependency-licences.json
python scripts/check_dependency_licenses.py dependency-licences.json
```

The GitHub Actions workflow is the intended automated route; no local setup
is required for the repository check.

"""Read-only local environment check for Coconut Harvest AI.

This script does not install packages, download models, use the network,
or change system settings. Run with: python scripts/check_local_environment.py
"""
from __future__ import annotations

import importlib.util
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    print("Coconut Harvest AI — local environment check")
    print("=" * 48)
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {platform.python_version()}")
    print(f"Operating system: {platform.platform()}")

    try:
        disk = shutil.disk_usage(Path.cwd())
        print(f"Free disk space on current drive: {disk.free / (1024**3):.1f} GiB")
    except OSError as exc:
        print(f"Disk space: unavailable ({exc})")

    print("\nInstalled Python packages (checked without installing anything):")
    for package in ("torch", "transformers", "accelerate", "numpy", "pytest"):
        available = importlib.util.find_spec(package) is not None
        print(f"  {package}: {'available' if available else 'not found'}")

    print("\nNVIDIA command-line check:")
    nvidia_smi = shutil.which("nvidia-smi")
    if not nvidia_smi:
        print("  nvidia-smi was not found on PATH.")
        print("  This does not prove the GPU is absent; check the NVIDIA driver.")
    else:
        try:
            result = subprocess.run(
                [
                    nvidia_smi,
                    "--query-gpu=name,memory.total,driver_version",
                    "--format=csv,noheader",
                ],
                capture_output=True,
                text=True,
                timeout=8,
                check=False,
            )
            if result.returncode == 0:
                print("  GPU, total VRAM, driver:")
                print("  " + result.stdout.strip().replace("\n", "\n  "))
            else:
                print(f"  nvidia-smi returned code {result.returncode}.")
                if result.stderr.strip():
                    print("  " + result.stderr.strip())
        except (OSError, subprocess.TimeoutExpired) as exc:
            print(f"  Could not run nvidia-smi: {exc}")

    print("\nPyTorch CUDA check:")
    if importlib.util.find_spec("torch") is None:
        print("  PyTorch is not installed in this Python environment.")
        print("  No package was installed by this script.")
    else:
        try:
            import torch

            print(f"  PyTorch version: {torch.__version__}")
            print(f"  PyTorch CUDA build: {torch.version.cuda}")
            print(f"  CUDA available: {torch.cuda.is_available()}")
            if torch.cuda.is_available():
                device = torch.cuda.current_device()
                props = torch.cuda.get_device_properties(device)
                print(f"  CUDA device: {props.name}")
                print(f"  Total GPU memory: {props.total_memory / (1024**3):.2f} GiB")
        except Exception as exc:  # diagnostic reports rather than hides environment problems
            print(f"  PyTorch check failed: {type(exc).__name__}: {exc}")

    print("\nCost and safety:")
    print("  This script makes no network requests and installs nothing.")
    print("  It does not download model weights or send robot commands.")
    print("  It does not enable paid services or cloud billing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

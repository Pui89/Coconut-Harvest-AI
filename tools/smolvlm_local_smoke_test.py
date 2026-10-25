#!/usr/bin/env python3
"""Run one exploratory SmolVLM inference using already-present local files only.

This script never downloads a model, installs packages, calls a hosted endpoint,
or controls hardware. Use a local, permissioned image and treat output as text
for human review, not as a detector result or command.
"""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MODEL_ID = "HuggingFaceTB/SmolVLM-256M-Instruct"


def available_ram_gib() -> float | None:
    """Return available physical RAM without a third-party dependency."""
    try:
        if os.name == "nt":
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]
            status = MEMORYSTATUSEX()
            status.dwLength = ctypes.sizeof(status)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
                return status.ullAvailPhys / (1024 ** 3)
        page_size = os.sysconf("SC_PAGE_SIZE")
        available_pages = os.sysconf("SC_AVPHYS_PAGES")
        return page_size * available_pages / (1024 ** 3)
    except (AttributeError, OSError, ValueError):
        return None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def model_manifest(model_dir: Path) -> dict[str, Any]:
    files = sorted(p for p in model_dir.rglob("*") if p.is_file())
    lines = [f"{p.relative_to(model_dir).as_posix()}\t{p.stat().st_size}" for p in files]
    encoded = "\n".join(lines).encode("utf-8")
    return {
        "file_count": len(files),
        "total_file_bytes": sum(p.stat().st_size for p in files),
        "manifest_sha256": hashlib.sha256(encoded).hexdigest(),
        "files": [{"path": p.relative_to(model_dir).as_posix(), "bytes": p.stat().st_size} for p in files],
    }


def run_local_smoke_test(
    model_dir: Path,
    image_path: Path,
    prompt: str,
    max_new_tokens: int = 64,
    device_request: str = "cpu",
) -> dict[str, Any]:
    if not model_dir.is_dir():
        raise FileNotFoundError("MODEL_DIRECTORY_MISSING: provide a fully populated local model directory.")
    if not image_path.is_file():
        raise FileNotFoundError("IMAGE_FILE_MISSING: choose a local image you are permitted to use.")
    if not prompt.strip():
        raise ValueError("prompt must not be empty")
    if not 1 <= max_new_tokens <= 128:
        raise ValueError("max_new_tokens must be between 1 and 128")
    if device_request not in {"cpu", "cuda"}:
        raise ValueError("device_request must be 'cpu' or 'cuda'")

    required = ("config.json", "model.safetensors", "preprocessor_config.json")
    missing = [name for name in required if not (model_dir / name).is_file()]
    if missing:
        raise FileNotFoundError(
            "LOCAL_MODEL_FILES_MISSING: " + ", ".join(missing)
            + ". The tool will not fetch missing files."
        )

    ram_free_gib = available_ram_gib()
    if ram_free_gib is None:
        raise RuntimeError("RAM_PREFLIGHT_UNKNOWN: cannot read available system RAM; run the resource preflight first.")
    if ram_free_gib < 4.0:
        raise RuntimeError(
            f"RAM_PREFLIGHT_BLOCKED: only {ram_free_gib:.2f} GiB available; "
            "free memory before loading the model or defer this experiment."
        )

    # Set offline flags before importing Hugging Face libraries.
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

    try:
        import torch
        from PIL import Image
        import transformers
        from transformers import AutoModelForVision2Seq, AutoProcessor
    except ImportError as exc:
        raise RuntimeError(
            "DEPENDENCIES_MISSING: install compatible torch, transformers, Pillow and accelerate "
            "manually in an isolated local environment only after reviewing licence and disk/RAM/VRAM."
        ) from exc

    if device_request == "cuda":
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA_REQUESTED_BUT_UNAVAILABLE: rerun with --device cpu.")
        free_bytes, total_bytes = torch.cuda.mem_get_info()
        free_vram_gib = free_bytes / (1024**3)
        if free_vram_gib < 1.5:
            raise RuntimeError(
                f"CUDA_PREFLIGHT_BLOCKED: only {free_vram_gib:.2f} GiB free VRAM; "
                "use --device cpu or close GPU workloads."
            )
        device = "cuda"
        device_summary = {
            "requested": "cuda",
            "gpu_name": torch.cuda.get_device_name(0),
            "free_vram_gib_before_load": round(free_vram_gib, 3),
            "total_vram_gib": round(total_bytes / (1024**3), 3),
            "available_ram_gib_before_load": round(ram_free_gib, 3),
        }
    else:
        device = "cpu"
        device_summary = {"requested": "cpu", "note": "CPU selected to reduce VRAM pressure.", "available_ram_gib_before_load": round(ram_free_gib, 3)}

    manifest = model_manifest(model_dir)
    model_weight_sha256 = sha256_file(model_dir / "model.safetensors")
    image_sha256 = sha256_file(image_path)
    started = time.perf_counter()
    with Image.open(image_path) as source:
        image = source.convert("RGB")
    processor = None
    model = None
    try:
        processor = AutoProcessor.from_pretrained(
            str(model_dir), local_files_only=True, trust_remote_code=False
        )
        model = AutoModelForVision2Seq.from_pretrained(
            str(model_dir),
            local_files_only=True,
            trust_remote_code=False,
            low_cpu_mem_usage=True,
        )
        model.to(device)
        model.eval()
        messages = [{
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": prompt},
            ],
        }]
        text = processor.apply_chat_template(messages, add_generation_prompt=True)
        inputs = processor(text=text, images=[image], return_tensors="pt")
        inputs = {name: value.to(device) for name, value in inputs.items()}
        with torch.inference_mode():
            output_ids = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
        input_len = inputs["input_ids"].shape[1]
        generated = output_ids[:, input_len:]
        output_text = processor.batch_decode(generated, skip_special_tokens=True)[0].strip()
        elapsed_ms = round((time.perf_counter() - started) * 1000.0, 3)
        report = {
            "schema_version": 1,
            "status": "COMPLETED_EXPLORATORY_LOCAL_SMOKE_TEST",
            "model_id": MODEL_ID,
            "model_directory": str(model_dir.resolve()),
            "model_manifest": manifest,
            "model_safetensors_sha256": model_weight_sha256,
            "image_path": str(image_path.resolve()),
            "image_sha256": image_sha256,
            "image_dimensions": list(image.size),
            "prompt": prompt,
            "max_new_tokens": max_new_tokens,
            "software": {
                "python": platform.python_version(),
                "torch": torch.__version__,
                "transformers": transformers.__version__,
                "pillow": getattr(__import__("PIL"), "__version__", "unknown"),
            },
            "device": device_summary,
            "observed_latency_ms": elapsed_ms,
            "generated_text": output_text,
            "download_performed": False,
            "hardware_actuation": False,
            "interpretation_limit": (
                "One exploratory generation only; not a detector benchmark or evidence of "
                "task accuracy. Human review is required. VLM output is not an action command."
            ),
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
        }
        return report
    finally:
        del model
        del processor
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-dir", type=Path, required=True, help="Existing local model directory; never downloaded.")
    parser.add_argument("--image", type=Path, required=True, help="Existing local image file.")
    parser.add_argument("--prompt", default="Describe only the visible objects and scene. State uncertainty; do not infer hidden contents.")
    parser.add_argument("--max-new-tokens", type=int, default=64)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--output", type=Path, default=Path("reports/smolvlm-local-smoke.json"))
    args = parser.parse_args()
    try:
        report = run_local_smoke_test(
            args.model_dir, args.image, args.prompt, args.max_new_tokens, args.device
        )
    except (OSError, RuntimeError, ValueError, ImportError) as exc:
        print(f"SMOLVLM_LOCAL_SMOKE_TEST_BLOCKED: {exc}", file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"status={report['status']} model={report['model_id']} download_performed=false hardware_actuation=false")
    print(f"report={args.output}")
    print("Output is an exploratory caption, not a detector result or action command.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

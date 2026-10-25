"""Deterministic experiment report helpers; standard library only."""
from __future__ import annotations
import math
from statistics import mean, median
from typing import Any, Mapping, Sequence

def _finite_number(value: Any) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value)

def build_experiment_report(*, project: str, run_id: str, code_version: str, dataset_sha256: str,
                            metrics: Mapping[str, int | float], latency_ms: Sequence[int | float] = (),
                            repeatability_runs: Sequence[Mapping[str, int | float]] = (),
                            notes: Sequence[str] = ()) -> dict[str, Any]:
    """Summarize supplied measurements; does not run experiments or invent missing values."""
    for name, value in (("project", project), ("run_id", run_id), ("code_version", code_version)):
        if not isinstance(value, str) or not value.strip(): raise ValueError(f"{name} must be non-empty text")
    if not isinstance(dataset_sha256, str) or len(dataset_sha256) != 64 or any(c not in "0123456789abcdef" for c in dataset_sha256.lower()):
        raise ValueError("dataset_sha256 must be a 64-character hexadecimal digest")
    clean = {}
    for key, value in metrics.items():
        if not isinstance(key, str) or not key.strip() or not _finite_number(value):
            raise ValueError("metric names must be non-empty and values finite numbers")
        clean[key] = value
    timings = list(latency_ms)
    if any(not _finite_number(v) or v < 0 for v in timings):
        raise ValueError("latency_ms values must be finite and non-negative")
    repeats = list(repeatability_runs)
    for run in repeats:
        if any(not isinstance(k, str) or not k.strip() or not _finite_number(v) for k, v in run.items()):
            raise ValueError("repeatability metrics must have named finite numeric values")
    latency = None
    if timings:
        ordered = sorted(float(v) for v in timings)
        latency = {"sample_count": len(ordered), "mean_ms": mean(ordered), "median_ms": median(ordered),
                   "p95_ms_nearest_rank": ordered[max(0, math.ceil(0.95 * len(ordered)) - 1)], "max_ms": ordered[-1]}
    return {"schema_version": 1, "project": project.strip(), "run_id": run_id.strip(),
            "code_version": code_version.strip(), "dataset_sha256": dataset_sha256.lower(),
            "metrics": dict(sorted(clean.items())), "latency": latency, "repeatability_runs": repeats,
            "notes": list(notes), "limitations": [
                "This report summarizes supplied measurements; it does not execute or validate a model.",
                "Metrics require documented provenance, split policy, and test conditions.",
                "Missing measurements are not inferred or fabricated."]}

#!/usr/bin/env python3
"""Reproducible, dependency-free CPU microbenchmark for adaptive task selection.

This is an engineering harness, not an AI model benchmark. It compares equivalent
integer-reduction implementations and reports local timing only; it does not infer
energy use, model quality, or hardware safety.
"""
from __future__ import annotations

import argparse
import json
import platform
import statistics
import sys
import time
from typing import Callable


def loop_sum(size: int) -> int:
    total = 0
    for value in range(size):
        total += value
    return total


def builtin_sum(size: int) -> int:
    return sum(range(size))


def adaptive_sum(size: int, threshold: int) -> int:
    """Select an implementation using an explicit, inspectable size threshold."""
    if size < threshold:
        return loop_sum(size)
    return builtin_sum(size)


def _measure(fn: Callable[[], int], repeats: int) -> dict[str, float | int]:
    fn()  # warm-up, excluded from reported samples
    samples_ms = []
    result = 0
    for _ in range(repeats):
        started = time.perf_counter_ns()
        result = fn()
        samples_ms.append((time.perf_counter_ns() - started) / 1_000_000)
    return {
        "result": result,
        "median_ms": round(statistics.median(samples_ms), 6),
        "min_ms": round(min(samples_ms), 6),
        "max_ms": round(max(samples_ms), 6),
        "samples_ms": [round(value, 6) for value in samples_ms],
    }


def run_benchmark(size: int, repeats: int, threshold: int) -> dict:
    # bool is a subclass of int in Python; reject it explicitly alongside floats.
    if type(size) is not int or size < 0:
        raise ValueError("size must be a non-negative integer")
    if type(repeats) is not int or repeats < 1:
        raise ValueError("repeats must be a positive integer")
    if type(threshold) is not int or threshold < 1:
        raise ValueError("threshold must be a positive integer")

    reference = size * (size - 1) // 2
    results = {
        "loop": _measure(lambda: loop_sum(size), repeats),
        "builtin": _measure(lambda: builtin_sum(size), repeats),
        "adaptive": _measure(lambda: adaptive_sum(size, threshold), repeats),
    }
    correctness = {name: item["result"] == reference for name, item in results.items()}
    return {
        "format": "pui89-adaptive-compute-cpu-benchmark-v1",
        "scope": "synthetic integer reduction; not an AI inference benchmark",
        "environment": {
            "python": sys.version.split()[0],
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "processor_label": platform.processor() or "not reported",
        },
        "workload": {
            "name": "sum_of_integer_range",
            "size": size,
            "repeats": repeats,
            "adaptive_threshold": threshold,
            "adaptive_choice": "loop" if size < threshold else "builtin",
        },
        "correctness": correctness,
        "all_outputs_match_reference": all(correctness.values()),
        "results": results,
        "interpretation_limits": [
            "Timing is specific to this machine, Python build, and current system load.",
            "This microbenchmark does not measure energy, model quality, or real-time guarantees.",
            "The size threshold is a configurable rule, not a learned policy.",
            "Repeat on representative workloads before drawing engineering conclusions.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", type=int, default=100_000, help="number of integers (default: 100000)")
    parser.add_argument("--repeats", type=int, default=7, help="timed samples per strategy (default: 7)")
    parser.add_argument(
        "--threshold",
        type=int,
        default=1_000,
        help="adaptive selector threshold; below it use loop, otherwise built-in sum",
    )
    args = parser.parse_args()
    try:
        report = run_benchmark(args.size, args.repeats, args.threshold)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["all_outputs_match_reference"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

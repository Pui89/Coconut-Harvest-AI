# Adaptive Compute CPU Benchmark (Research Harness)

**Status:** initial research harness; not a validated AI or robotics performance benchmark.

This dependency-free script establishes a reproducible starting point for discussing adaptive compute. It compares three equivalent integer-reduction strategies on the machine where it is run:

- `loop`: explicit Python loop
- `builtin`: Python's built-in `sum(range(n))`
- `adaptive`: a transparent size-threshold rule that selects one of the above

All strategies are checked against the exact arithmetic-series result. Timings include warm-up exclusion and report every measured sample plus median/minimum/maximum. The JSON records Python and platform information.

## Run locally

Requires Python 3.10+ and uses only the standard library:

```bash
python tools/adaptive_compute_benchmark.py --size 100000 --repeats 7 --threshold 1000 > adaptive-benchmark.json
python -m pytest tests/test_adaptive_compute_benchmark.py
```

Use multiple sizes and thresholds. Keep the raw JSON with the commit, machine details, and command line when comparing runs. Avoid comparing results from different machines as if they were a controlled experiment.

## What this does not prove

- It is **not** an AI inference, perception, robotics, or neuromorphic benchmark.
- The threshold is a hand-set rule, not a learned or novel policy.
- It does not measure energy, accelerator utilization, safety, model accuracy, or hard real-time guarantees.
- A microbenchmark result alone is not evidence that an adaptive policy will help Coconut Harvest AI, Flood Rescue AI, or Multimodal Narcotics Screening AI.

## Research progression

1. Establish repeatable baselines across workload sizes and report variance.
2. Add representative, licensed workloads from each project and preserve output-quality checks.
3. Define resource budgets and compare fixed versus adaptive execution on the same workload set.
4. Inject missing/invalid inputs and verify that safety controls remain independent of performance scheduling.
5. Consider event-driven or neuromorphic-inspired algorithms only if measurements identify a relevant bottleneck.

No hardware or paid service is required for this initial stage.

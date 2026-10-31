# Coconut Harvest — PUI89 Project Model Adapter

**Status:** mock-only; model inference is disabled.

The adapter is `tools/pui89_coconut_model_adapter.py`. It accepts only caller-supplied synthetic fixture observations and validates one of four candidate labels: `young_green`, `developing`, `mature_green`, or `brown_aging`.

Each accepted fixture is returned as an unverified candidate maturity cue for human review. The adapter does not inspect images, run a detector, establish harvest readiness, or authorize climbing, cutting, capture or robot movement.

Evidence must be explicitly marked `synthetic`, use a `synthetic://` source reference, include timestamp and lineage, and not be future-dated relative to the request. Physical command fields are rejected.

Run tests: `PYTHONPATH=tools python -m unittest discover -s tests -p "test_pui89_coconut_model_adapter.py" -v`.

No model weights, third-party packages, network calls, paid APIs, cloud GPUs or hardware are used. This tests the adapter contract only; it is not evidence of AI maturity-classification performance.
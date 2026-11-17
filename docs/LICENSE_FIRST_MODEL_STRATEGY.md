# Coconut Harvest AI — Model Selection and Licence Gate

## Current decision

No object-detection framework or checkpoint is selected or approved for this project. The previous detector integration has been retired from the active codebase. Do not install detector-specific packages or download model weights.

## Required review before any future selection

A candidate must pass all of the following before adoption:

1. Exact code licence and version, including transitive dependencies.
2. Exact checkpoint/weight licence and redistribution conditions.
3. Model and dataset provenance, source and integrity checks.
4. Security review of model loading and serialization format.
5. CPU-only feasibility, peak RAM, model size and measured latency on available equipment.
6. Reproducible evaluation on a rights-cleared, human-verified coconut dataset.
7. Per-class precision, recall, F1, confusion matrix, sample counts and failure analysis.
8. Clear distinction between research use, redistribution and commercial deployment rights.

A permissive code licence does not automatically establish that model weights or training data have compatible terms. Public availability is not permission to reuse.

## Current project path

Continue with licensed real-image collection, human annotation, annotation QA, group-separated splits and the CPU-first four-class appearance baseline. Keep detector selection as a separate future engineering gate.

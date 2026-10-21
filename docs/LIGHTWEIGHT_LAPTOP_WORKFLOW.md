# Lightweight, Laptop-Friendly Research Workflow

This project is designed to make useful progress without assuming a powerful laptop or paid compute. It is a workflow guide, not a claim that all experiments have been run.

## What can run without a GPU?

| Task | Typical compute need | Recommendation |
|---|---|---|
| Unit tests and input validation | Low; CPU | Run first |
| CSV/JSON evaluation and SHA-256 audits | Low; CPU | Use local Python |
| Manual annotation and image review | Low to moderate | Work with a small image batch |
| Detector inference with existing weights | Model-dependent | Try only after checking RAM, disk, dependencies and licence |
| Fine-tuning or training large vision-language models | Potentially high | Do not start on a constrained laptop |

Actual runtime depends on the laptop, Python environment, image size, and chosen model.

## Recommended order

1. Check available disk space and RAM; do not install large packages yet.
2. Run the repository's lightweight unit tests first:
   `python -m unittest discover -s tests -v`
3. Fix failing tests before adding features. Save the command output and commit SHA.
4. Review a small set of legally usable images and human-check annotations.
5. Choose a detector only after checking whether the machine can run it and whether the model licence permits the intended use.
6. If inference is too demanding, report **model inference not yet run on available hardware**. Continue with CPU-based tests, data-quality audits, evaluation-tool tests, and documented experiment design.
7. Keep benchmark inputs, predictions and outputs versioned locally or as permitted; do not commit private or unlicensed images or weights.

## What this workflow does not promise

- It does not make a large model fit into limited RAM.
- It does not replace actual detector inference with synthetic predictions.
- Passing tests is software evidence, not proof of model accuracy or robot performance.
- Do not use paid cloud compute, APIs, or services without explicit budget approval.

## Minimal information to record

- Laptop OS, RAM and free disk space
- Python version
- Exact test/inference command
- Exit status and full error message if a command fails
- Git commit SHA and output files

## Research framing

A constrained-compute study can still be rigorous when its scope is explicit: evaluate software correctness, data quality, reproducibility, uncertainty, and limitations. Any claims about real-world detection must wait for actual inference on suitable held-out data.

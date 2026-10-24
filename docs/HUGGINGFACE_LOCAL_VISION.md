# Hugging Face local vision experiment

## Purpose

This optional experiment uses the Hugging Face Transformers zero-shot object-detection pipeline to explore exploratory detection of visible coconuts and coconut bunches. It uses a pretrained model; it does not train a project-specific model.

## Free, local-first operation

- Run inference locally on an image path. The script does not call a hosted inference API or upload the image.
- The first run may download model weights from the Hugging Face Hub into the local cache. This uses internet bandwidth and disk space but not a paid inference service. Review the model card and licence before use.
- CPU is the default to reduce GPU-memory pressure. CUDA must be requested explicitly.
- The script never installs packages automatically. Use a project virtual environment and a Python/PyTorch combination supported by the selected versions.
- Predictions and annotated images are written only when you supply the relevant output options.

## Setup

Install compatible local versions of PyTorch, Transformers and Pillow in your existing virtual environment. Do not install them globally or use a paid hosted inference endpoint.

## Run

From the repository root on Windows:

```powershell
python tools/huggingface_local_vision_demo.py "path\to\your-image.jpg"
```

Save results if needed:

```powershell
python tools/huggingface_local_vision_demo.py "path\to\your-image.jpg" --json-out "outputs\hf-preview.json" --annotated-image "outputs\hf-preview.jpg"
```

Use repeated `--label` arguments to replace the default candidate labels. For example:

```powershell
python tools/huggingface_local_vision_demo.py "path\to\your-image.jpg" --label "visible object" --label "background object"
```

To request CUDA explicitly, add `--device cuda`; if memory is insufficient, rerun on CPU. Model downloads can be large, so do not run the script unless you want to download the selected checkpoint.

## Evidence and limitations

A pretrained open-vocabulary model may miss coconuts or draw incorrect boxes, especially for small, overlapping, occluded or distant fruit. Outputs are not training labels and do not change the dataset approval gate. Do not use detections to command a cutter or robot arm.

- Scores are model confidence-like scores, not calibrated probabilities.
- This experiment is not a benchmark. Do not report precision, recall, mAP, field reliability, or safety performance from a single image.
- Keep exploratory outputs separate from approved training data and formal evaluation sets.
- Check model-card licence, intended use, known limitations, and dependency licences before redistribution.
- This code is an opt-in experiment only; it does not change project hardware, autonomy, or safety-control behaviour.

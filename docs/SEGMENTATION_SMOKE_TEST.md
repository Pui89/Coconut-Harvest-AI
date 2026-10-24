# SAM 3 local segmentation smoke test

This optional smoke test checks whether the SAM 3 text-prompt image-segmentation pipeline can run on one image on your own computer. It is deliberately separate from the main application and does not control a robot.

## Important before running

- The script reads an image already on your computer; it does not download images or upload your image.
- Model files are downloaded from Hugging Face only when you run the script. They can be large and consume disk space and bandwidth.
- The model repository may be gated. You may need to sign in to Hugging Face, request/accept the applicable access terms, and use a permitted account token. Do not paste tokens into chat or commit them to Git.
- Check the model's current licence and usage terms before use. This workflow is intended to be free/local-first; do not enable paid cloud services.
- The script uses CUDA when PyTorch reports it available, otherwise CPU. CPU inference may be slow; GPU memory limitations can cause out-of-memory errors.
- A successful smoke test is not evidence of project accuracy, safe autonomy, or field readiness.

## 1. Create and activate a virtual environment

Use Python 3.11 or 3.12 for the first compatibility attempt, if available.

Windows PowerShell:

```powershell
py -3.11 -m venv .venv-sam3
.\.venv-sam3\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Install a PyTorch build suitable for your computer from the official PyTorch install selector, then install the compatible Transformers version and Pillow:

```powershell
python -m pip install "transformers>=5.0.0" pillow
```

If the installed Transformers release does not expose SAM 3 through AutoProcessor/AutoModel, stop and check the current official Hugging Face SAM 3 model card rather than installing random forks.

## 2. Run against a local image

Choose an image you have permission to use. Replace the example path and prompt with a real local path and a task-specific phrase.

```powershell
python tools/sam3_smoke_test.py --image "C:\path\to\your-image.jpg" --prompt "coconut"
```

Example prompts to try separately:
- Coconut project: `coconut`, `coconut cluster`, or `tree trunk`
- Flood project: `person`, `boat`, or `flood water`
- Screening project: `package`, `bag`, or `container`

Prompts are exploratory; they do not guarantee that the model recognizes the class correctly.

## 3. Inspect output

The script writes `artifacts/sam3-smoke-test/summary.json` and one binary PNG mask per returned instance. Check the image dimensions, instance count, confidence scores, and whether masks actually align with the intended objects.

Record the model ID/revision, Transformers/PyTorch versions, hardware, prompt, and any failures before comparing runs. Do not treat a zero-mask result as proof that an object is absent.

## Status

The repository includes a smoke-test script, not a claim that SAM 3 has already been downloaded or successfully run. Project-level validation remains **not measured** until someone runs it on licensed, reviewed examples and records results. Flood-water segmentation, coconut maturity, and concealed-substance screening require separate task-specific validation; a generic mask is not a diagnosis or detection of hidden contents.

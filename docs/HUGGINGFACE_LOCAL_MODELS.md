## Free local Hugging Face model plan

**Goal:** experiment locally with orchard-image understanding without paid APIs, hosted inference, cloud GPUs, or a subscription.

### Suggested model
- **Model ID:** [microsoft/Florence-2-base](https://huggingface.co/microsoft/Florence-2-base)
- **License shown on model card:** MIT. Review the model card and included license before use.
- **Tasks:** image captioning, phrase grounding, and general object-detection experiments.
- **Limit:** this is not a validated coconut detector. Coconut-specific accuracy requires labelled orchard images and held-out evaluation.

### Local setup
Use an existing Python environment and install PyTorch from the official [local installation selector](https://pytorch.org/get-started/locally/). Then install:
```bash
python -m pip install transformers accelerate pillow
```
Download the model once while online, then use cached files locally. First download can use disk space and internet data; inference does not require a paid hosted endpoint.

### Safe implementation order
1. Run captioning on a small set of permitted orchard images.
2. Add object-grounding tests and manually compare boxes with labelled coconuts.
3. Record model version, dataset provenance, precision/recall where applicable, latency, and failure cases.
4. Keep the existing prototype labelled as a prototype until tests demonstrate the capability.

### Zero-cost / no-surprise-bill policy
- Do not call Hugging Face Inference Providers or paid endpoints.
- Do not create a cloud GPU, paid notebook, or billing account.
- Do not add automatic downloads to CI; keep model weights out of Git unless explicitly necessary.
- Model download, local storage, electricity, and internet data are still resource costs.
- Review custom model code before using `trust_remote_code=True`.

### Status
This file is a model integration plan. It does not mean the model is already wired into the app or that results have been validated.
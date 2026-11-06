# Hugging Face vision-model integration

**Status: optional model adapters added; model weights are not downloaded and inference is not yet benchmarked in this repository.**

This project now has an opt-in local adapter at [`pui89_models/hf_vision.py`](../pui89_models/hf_vision.py). It connects to real Hugging Face model checkpoints rather than placeholder model names.

## Approved model checkpoints

| Checkpoint | Task | Licence shown on model card | Use in this project |
|---|---|---|---|
| [google/owlv2-base-patch16-ensemble](https://huggingface.co/google/owlv2-base-patch16-ensemble) | Text-conditioned, open-vocabulary object detection | Apache-2.0 | Candidate object localization for the project-specific research scope. |
| [depth-anything/Depth-Anything-V2-Small-hf](https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf) | Monocular relative-depth estimation | Apache-2.0 | Optional relative scene geometry only. |

Model-card licences are checkpoint-level information, not a blanket clearance for datasets, dependencies, downstream uses or every project jurisdiction. Recheck the model card, terms, provenance and security before release.

## Run locally — opt-in only

The adapter imports without importing or downloading ML packages. It requires compatible local installations of PyTorch, Transformers and Pillow (and NumPy for the depth-map output). No package installation is performed by this repository.

1. Run the project's standard-library verification first.
2. Install dependencies only after checking the current Python version, RAM, disk space, package licences and compatibility. CPU inference is the default.
3. Download model weights only after an explicit decision. By default, the loader uses the existing Hugging Face cache only.
4. To permit a direct Hugging Face Hub download, explicitly set `PUI89_ALLOW_MODEL_DOWNLOAD=1` in the current shell, or pass `allow_download=True` to a loader. This downloads weights to the local cache; it does not use hosted inference or a cloud GPU.
5. Keep model weights out of Git unless there is a separately approved reason.

Example:

```python
from PIL import Image
from pui89_models.hf_vision import detect_objects

image = Image.open("path/to/reviewed-image.jpg").convert("RGB")
proposals = detect_objects(
    image,
    labels=["person", "animal", "vehicle", "obstacle"],
    threshold=0.20,
)
print(proposals)
```

The first run fails clearly if the model is not already cached. It will not silently download anything. The detector returns candidate boxes and scores; thresholds must be calibrated on a lawful, representative, independently labelled evaluation set.

## Project-specific boundaries

- **OWLv2:** Candidate localization of coconut bunches, palm trunks, fronds, workers and obstacles. Maturity class (young / mature green / yellow / brown-aging) is not established by OWLv2 alone; require reviewed labels and a project-trained, held-out benchmark.
- **Depth Anything V2:** Optional relative scene geometry only. It cannot measure the palm's actual height, 0–30 m reach, bunch distance or safe cutter clearance.

## Important limitations

- OWLv2 is an open-vocabulary proposal model, not a project-trained detector. A text prompt does not establish that an object is present.
- Depth Anything V2 produces **relative monocular depth**, not calibrated metric distance. It must not be reported as exact range, flood depth, coconut height, clearance or braking distance.
- Neither model controls motors, steering, brakes, cutters, valves, alarms, locks or other actuators.
- Preserve source, timestamp, image quality, model ID/revision, prompt, threshold, raw output, uncertainty and human-review outcome in the project's evidence records.
- Unknown, conflicting, low-quality or out-of-distribution results must remain unknown and go to human review.
- No real-world accuracy, safety, certification or product capability is claimed by adding this adapter.

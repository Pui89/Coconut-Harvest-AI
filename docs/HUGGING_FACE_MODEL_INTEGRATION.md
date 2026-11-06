# Hugging Face vision-model integration

**Status: optional model adapters added; model weights are not downloaded and inference is not yet benchmarked in this repository.**

This project now has an opt-in local adapter at [`pui89_models/hf_vision.py`](../pui89_models/hf_vision.py). It connects to real Hugging Face model checkpoints rather than placeholder model names.

## Approved model checkpoints

| Checkpoint | Task | Licence shown on model card | Use in this project |
|---|---|---|---|
| [google/owlv2-base-patch16-ensemble](https://huggingface.co/google/owlv2-base-patch16-ensemble) | Text-conditioned, open-vocabulary object detection | Apache-2.0 | Candidate object localization for the project-specific research scope. |
| [Intel/dpt-hybrid-midas](https://huggingface.co/Intel/dpt-hybrid-midas) | Monocular relative-depth estimation | Apache-2.0 | Optional relative scene geometry only. |

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
- **Intel DPT-Hybrid:** Optional relative scene geometry only. It cannot measure the palm's actual height, 0–30 m reach, bunch distance or safe cutter clearance.

## Important limitations

- OWLv2 is an open-vocabulary proposal model, not a project-trained detector. A text prompt does not establish that an object is present.
- Intel DPT-Hybrid produces **relative monocular depth**, not calibrated metric distance. It must not be reported as exact range, flood depth, coconut height, clearance or braking distance.
- Neither model controls motors, steering, brakes, cutters, valves, alarms, locks or other actuators.
- Preserve source, timestamp, image quality, model ID/revision, prompt, threshold, raw output, uncertainty and human-review outcome in the project's evidence records.
- Unknown, conflicting, low-quality or out-of-distribution results must remain unknown and go to human review.
- No real-world accuracy, safety, certification or product capability is claimed by adding this adapter.


## Robotics VLA research checkpoint — arm manipulation only

The project also records [`lerobot/smolvla_base`](https://huggingface.co/lerobot/smolvla_base), a real 450M-parameter Vision-Language-Action checkpoint released under Apache-2.0. It is a research starting point for manipulation, not a ready-made coconut-harvesting policy. The model card describes it as a base model intended to be fine-tuned to a specific task.

An opt-in loader is provided at [`pui89_models/smolvla.py`](../pui89_models/smolvla.py). It uses local cache only by default and returns unexecuted action proposals. It does not connect to hardware. A compatible LeRobot observation/action schema, representative robot-arm dataset, fine-tuning, simulator, safety case and independent evaluation are required. It is not evidence that the proposed 0–30 m arm or harvesting system works.

"""Opt-in local Hugging Face vision adapters for PUI89 projects.

No model is downloaded at import time. By default, loaders only use model files
already present in the local Hugging Face cache. Set PUI89_ALLOW_MODEL_DOWNLOAD=1
or pass allow_download=True to permit a direct Hugging Face Hub download.
Inference is CPU-only by default and never calls a hosted inference API.
"""
from __future__ import annotations

import os
from typing import Iterable

OWLV2_MODEL_ID = "google/owlv2-base-patch16-ensemble"
DEPTH_MODEL_ID = "Intel/dpt-hybrid-midas"


def _local_only(allow_download: bool) -> bool:
    env_allows = os.environ.get("PUI89_ALLOW_MODEL_DOWNLOAD", "").strip() == "1"
    return not (allow_download or env_allows)


def load_owlv2(*, allow_download: bool = False):
    """Load OWLv2 for open-vocabulary object proposals.

    Requires torch, transformers and Pillow to be installed separately.
    """
    try:
        from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
    except ImportError as exc:
        raise RuntimeError(
            "OWLv2 dependencies are missing. Install reviewed, compatible "
            "versions of torch and transformers only after checking local "
            "hardware, package licences and disk space."
        ) from exc

    local_only = _local_only(allow_download)
    processor = AutoProcessor.from_pretrained(
        OWLV2_MODEL_ID, local_files_only=local_only
    )
    model = AutoModelForZeroShotObjectDetection.from_pretrained(
        OWLV2_MODEL_ID, local_files_only=local_only
    )
    model.eval()
    return processor, model


def detect_objects(image, labels: Iterable[str], *, threshold: float = 0.15,
                   allow_download: bool = False):
    """Return OWLv2 text-conditioned box proposals for a PIL image.

    Results are observations, not verified identities or safety decisions.
    """
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be between 0 and 1")
    labels = [str(label).strip() for label in labels if str(label).strip()]
    if not labels:
        raise ValueError("provide at least one non-empty text label")

    import torch

    processor, model = load_owlv2(allow_download=allow_download)
    inputs = processor(text=[labels], images=image, return_tensors="pt")
    with torch.inference_mode():
        outputs = model(**inputs)
    target_sizes = torch.tensor([image.size[::-1]])
    result = processor.post_process_object_detection(
        outputs, threshold=threshold, target_sizes=target_sizes
    )[0]

    scores = result["scores"].detach().cpu().tolist()
    label_ids = result["labels"].detach().cpu().tolist()
    boxes = result["boxes"].detach().cpu().tolist()
    return [
        {
            "label": labels[label_id],
            "score": float(score),
            "box_xyxy": [float(v) for v in box],
            "status": "MODEL_PROPOSAL_REQUIRES_REVIEW",
        }
        for score, label_id, box in zip(scores, label_ids, boxes)
    ]


def load_depth_anything_v2(*, allow_download: bool = False):
    """Load the small Transformers-compatible Depth Anything V2 checkpoint."""
    try:
        from transformers import AutoImageProcessor, AutoModelForDepthEstimation
    except ImportError as exc:
        raise RuntimeError(
            "Depth model dependencies are missing. Install reviewed, compatible "
            "versions of torch and transformers only after checking hardware, "
            "package licences and disk space."
        ) from exc

    local_only = _local_only(allow_download)
    processor = AutoImageProcessor.from_pretrained(
        DEPTH_MODEL_ID, local_files_only=local_only
    )
    model = AutoModelForDepthEstimation.from_pretrained(
        DEPTH_MODEL_ID, local_files_only=local_only
    )
    model.eval()
    return processor, model


def estimate_relative_depth(image, *, allow_download: bool = False):
    """Return a relative-depth map; values are not metric distance or water depth."""
    import torch
    import torch.nn.functional as F

    processor, model = load_depth_anything_v2(allow_download=allow_download)
    inputs = processor(images=image, return_tensors="pt")
    with torch.inference_mode():
        outputs = model(**inputs)
        depth = F.interpolate(
            outputs.predicted_depth.unsqueeze(1),
            size=(image.height, image.width),
            mode="bicubic",
            align_corners=False,
        ).squeeze()
    return depth.detach().cpu().numpy()


__all__ = [
    "OWLV2_MODEL_ID",
    "DEPTH_MODEL_ID",
    "load_owlv2",
    "detect_objects",
    "load_depth_anything_v2",
    "estimate_relative_depth",
]

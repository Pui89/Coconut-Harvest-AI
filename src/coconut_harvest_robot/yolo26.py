from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Any

import numpy as np


@dataclass
class YOLO26Detection:
    """Normalized YOLO26 detection record for orchard perception."""

    class_id: int
    class_name: str
    confidence: float
    xyxy: tuple[float, float, float, float]


class YOLO26Detector:
    """Optional YOLO26 detector loaded from the official Hugging Face repo.

    YOLO26 is used as the fast visual proposal layer. It does not decide
    ripeness, reachability, harvesting, or physical actuation.
    """

    HF_REPO = "Ultralytics/YOLO26"
    HF_REVISION = "4558807"  # Upstream model repository revision observed 2026-10-22.

    def __init__(
        self,
        weights: str = "yolo26n.pt",
        confidence: float = 0.35,
        imgsz: int = 640,
        device: str | int | None = None,
    ) -> None:
        try:
            from huggingface_hub import hf_hub_download
            from ultralytics import YOLO
        except ImportError as exc:
            raise ImportError(
                "YOLO26 requires 'ultralytics' and 'huggingface-hub'. "
                "Install the project dependencies first."
            ) from exc

        self.confidence = confidence
        self.imgsz = imgsz
        self.device = device
        self.weights = weights
        # Cache-only by default. Set PUI89_ALLOW_MODEL_DOWNLOAD=1 only after
        # reviewing the weight size, license, and network use.
        allow_download = os.getenv("PUI89_ALLOW_MODEL_DOWNLOAD", "").strip().lower() in {
            "1", "true", "yes"
        }
        self.weights_path = hf_hub_download(
            self.HF_REPO, weights, revision=self.HF_REVISION, local_files_only=not allow_download
        )
        self.model = YOLO(self.weights_path)

    @staticmethod
    def _to_numpy(image: Any) -> np.ndarray:
        if hasattr(image, "detach"):
            image = image.detach().cpu()
            if image.ndim == 4:
                image = image[0]
            if image.ndim == 3 and image.shape[0] in (1, 3, 4):
                image = image.permute(1, 2, 0)
            image = image.numpy()
        image = np.asarray(image)
        if image.ndim != 3:
            raise ValueError("Expected an RGB image with shape [H, W, C] or [C, H, W].")
        if image.dtype != np.uint8:
            if image.max() <= 1.0:
                image = image * 255.0
            image = np.clip(image, 0, 255).astype(np.uint8)
        if image.shape[-1] == 1:
            image = np.repeat(image, 3, axis=-1)
        if image.shape[-1] != 3:
            raise ValueError("YOLO26 expects a 3-channel RGB image.")
        return image

    def predict(self, image: Any) -> list[YOLO26Detection]:
        """Return visual proposals without issuing any robot command."""
        frame = self._to_numpy(image)
        kwargs = {"conf": self.confidence, "imgsz": self.imgsz, "verbose": False}
        if self.device is not None:
            kwargs["device"] = self.device
        results = self.model.predict(frame, **kwargs)

        detections: list[YOLO26Detection] = []
        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue
            names = result.names
            xyxy = boxes.xyxy.detach().cpu().numpy()
            conf = boxes.conf.detach().cpu().numpy()
            cls = boxes.cls.detach().cpu().numpy().astype(int)
            for box, score, class_id in zip(xyxy, conf, cls):
                detections.append(
                    YOLO26Detection(
                        class_id=class_id,
                        class_name=str(names[int(class_id)]),
                        confidence=float(score),
                        xyxy=tuple(float(v) for v in box),
                    )
                )
        return detections

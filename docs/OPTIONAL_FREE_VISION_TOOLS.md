# Optional Free Vision and Dataset Resources

This guide adds optional tools around the existing Coconut Harvest AI dataset audits and detector benchmarks. It does not replace the project's annotation, manifest-hash, leakage-audit or dataset-promotion gates.

## Recommended order

1. **OpenCV** — optional local image-quality and geometry utilities for detecting unreadable images, recording image dimensions, reviewing brightness/blur and generating visual QA overlays. It does not identify maturity or approve a coconut for harvesting.
2. **CVAT Community** — optional self-hosted annotation/review UI for bounding boxes and maturity labels. Prefer local deployment when the laptop can support it; do not put private images into a hosted service without checking terms and data rights.
3. **Open3D** — later, only when real depth or point-cloud data is available for canopy/fruit geometry. It is not needed for the current RGB-only path.
4. **OpenVINO** — later CPU-inference option to benchmark against the existing local baseline, not a promised speed-up.
5. **Tesseract OCR** — low priority for coconut detection; use only if a workflow genuinely needs visible text extraction from equipment labels or metadata cards.

## Free-resource register

| Resource | Local check | Licence note | Official source |
|---|---|---|---|
| OpenCV Python (cv2) | Python module | OpenCV 4.5.0+ is Apache-2.0; older releases have different terms and bundled dependencies may differ. | [Licence](https://opencv.org/license/) · [Project](https://github.com/opencv/opencv) |
| CVAT Community | Manual/self-hosted service check | Community core is MIT; review FFmpeg and third-party asset/dependency licences too. | [Community repository](https://github.com/cvat-ai/cvat) · [Licence overview](https://docs.cvat.ai/docs/getting_started/overview/) |
| Open3D | Python module (open3d) | MIT. Check the exact release and bundled dependencies. | [Project and licence](https://www.open3d.org/) |
| Tesseract OCR engine | tesseract executable | Apache-2.0; language data and distribution packages have their own details. | [Official documentation](https://tesseract-ocr.github.io/tessdoc/) |
| OpenVINO | Python module (openvino) | Apache-2.0 toolkit; model weights retain their own licences. | [Official repository](https://github.com/openvinotoolkit/openvino) |

## Check what is already available

Run from the repository root:

    python tools/check_optional_resources.py

The command emits JSON to the terminal and checks only local module metadata/PATH entries. It makes no network requests, installs no packages and downloads no model weights. A resource marked **manual_check** (such as CVAT Community) is deliberately not treated as installed or running.

## Evidence boundary

All new vision tools remain optional; core dependencies are unchanged. Record the exact tool/version in experiments. Use fixed, leakage-safe train/validation/test splits by tree, orchard and capture session. Keep image rights, source URL, licence, SHA-256, human review and exclusions in the existing data records. Report detection precision/recall, per-maturity results and latency only after the relevant tests have actually run. Image QA scores are diagnostics, not detection metrics or harvest-safety decisions.

No install, model inference or benchmark is performed by the probe.
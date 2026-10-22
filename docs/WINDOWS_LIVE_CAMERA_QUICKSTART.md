# Windows local webcam quick start

This workflow is free-first and runs on your Windows computer. It does not upload camera frames, download model weights, or send robot commands.

## 1. Open the repository folder

In File Explorer, open the extracted `Coconut-Harvest-AI` folder. Click the address bar, type `cmd`, and press Enter. Confirm that `dir` shows `README.md` and the `apps` folder.

## 2. Check Python before installing anything

Run:

```bat
python --version
python scripts\check_local_environment.py
```

For optional PyTorch/Ultralytics inference on Windows, use a separate Python 3.12 environment rather than the previously reported Python 3.14 environment. PyTorch's current Windows guidance lists Python 3.9–3.12 support. Do not remove your existing Python installation.

If the `py` launcher lists Python 3.12, create an isolated environment:

```bat
py -3.12 -m venv .venv-coconut-live
.venv-coconut-live\Scripts\activate
python --version
python -m pip --version
```

If `py -3.12` is unavailable, stop here and install Python 3.12 from the official Python website, choosing the Windows installer. Keep the existing Python installation. Then repeat the commands above.

## 3. Camera preview only (no AI)

Install only OpenCV into this isolated environment:

```bat
python -m pip install opencv-python
python apps\pui89_app\live_camera_preview.py
```

A window should show the webcam feed with the label **CAMERA PREVIEW ONLY - NO AI DETECTION**. Press `q` while the camera window is focused to exit. If the camera cannot open, close other apps using it and try:

```bat
python apps\pui89_app\live_camera_preview.py --camera 1
```

This confirms camera access only. It does not identify coconuts.

## 4. Run the existing local image-upload app

Install the app's listed dependencies in the same virtual environment:

```bat
python -m pip install -r apps\pui89_app\requirements.txt
python -m streamlit run apps\pui89_app\web_demo.py
```

Open the local address printed by Streamlit in your browser and upload a permitted JPG/PNG/WebP image. The current app displays the image and runs manual-input decision rules; the uploaded photo is **not automatically analysed** unless a valid local model is configured.

## 5. Optional local coconut detection (only when you have trusted weights)

The repository does not currently include a trained coconut detector or dataset ready for training. Do not use a generic model as proof of coconut detection. Only proceed when you already have a trusted local `.pt` checkpoint whose class names explicitly include `coconut` or `coconuts`, and you have reviewed its source and licence.

Install optional inference packages only if you choose this step; PyTorch/Ultralytics can require several gigabytes and network downloads. Check free disk space first. The following command may download large packages from package indexes:

```bat
python -m pip install -r apps\pui89_app\requirements-detector.txt
```

Then pass the existing local checkpoint path:

```bat
python apps\pui89_app\live_camera_preview.py --model "C:\path\to\your_coconut_model.pt" --device cpu
```

Use `--device auto` only after confirming the installed PyTorch build and NVIDIA driver work together. Begin with CPU and `--imgsz 384`; performance may be slow. The script rejects a model that lacks an explicitly labelled coconut class and never falls back to downloading model weights.

For a still image, the current Streamlit app accepts uploaded photos. To enable its optional inference panel, set the environment variable to a trusted local model path before launching the app:

```bat
set PUI89_COCONUT_MODEL_PATH=C:\path\to\your_coconut_model.pt
python -m streamlit run apps\pui89_app\web_demo.py
```

## Troubleshooting and evidence limits

- `ModuleNotFoundError: cv2`: activate `.venv-coconut-live` and install `opencv-python`.
- Camera window is black or cannot open: close Teams/Zoom/browser camera tabs, check Windows camera privacy permissions, or try camera index 1.
- Model file missing or class label rejected: check the local file path and its model class names; do not substitute an unverified model.
- A visible box is only a model prediction. It does not establish accuracy, maturity, calibrated 3D location, reachability, collision safety, or permission to harvest.
- Do not connect this script to motors or cutters. Stop testing if the camera or model behaves unexpectedly.

This guide and script have been committed to the repository, but have not been executed on your computer by this change.

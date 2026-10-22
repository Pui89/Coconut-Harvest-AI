"""Local webcam preview with optional coconut-trained model inference.

This script runs on the local computer only. Without --model it shows camera
frames only. With --model it loads an existing trusted local .pt file and
requires an explicit coconut class. It never downloads weights or controls a robot.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default: 0)")
    parser.add_argument("--model", type=Path, default=None, help="Optional existing local coconut-trained .pt file")
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    parser.add_argument("--imgsz", type=int, choices=(384, 512, 640), default=384)
    parser.add_argument("--conf", type=float, default=0.25)
    args = parser.parse_args()

    try:
        import cv2
    except ImportError:
        print("ERROR: OpenCV is missing. Install the optional local detector requirements:")
        print("  python -m pip install -r apps/pui89_app/requirements-detector.txt")
        return 2

    model = None
    coconut_ids: set[int] = set()
    detect_coconuts = None
    if args.model is not None:
        if not args.model.is_file():
            print(f"ERROR: model file not found: {args.model}")
            return 2
        try:
            from PIL import Image
            from apps.pui89_app.local_detector import detect_coconuts as _detect, load_local_coconut_model
            model, coconut_ids = load_local_coconut_model(args.model)
            detect_coconuts = _detect
            print(f"Loaded local model: {args.model}")
            print(f"Coconut class IDs: {sorted(coconut_ids)}")
        except Exception as exc:
            print(f"ERROR: could not load trusted local coconut model: {type(exc).__name__}: {exc}")
            return 2
    else:
        Image = None
        print("CAMERA PREVIEW ONLY: no AI model loaded; no coconut detection will occur.")

    camera = cv2.VideoCapture(args.camera, cv2.CAP_DSHOW if sys.platform == "win32" else 0)
    if not camera.isOpened():
        camera.release()
        print(f"ERROR: could not open camera index {args.camera}. Close other camera apps or try --camera 1.")
        return 2

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    print("Press q in the camera window to quit. No robot commands are sent.")
    try:
        while True:
            ok, frame = camera.read()
            if not ok or frame is None:
                print("ERROR: camera frame unavailable; stopping preview.")
                break
            if model is not None:
                from PIL import Image
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                detections = detect_coconuts(
                    model, Image.fromarray(rgb), coconut_ids,
                    confidence=args.conf, image_size=args.imgsz, device=args.device,
                )
                for item in detections:
                    x1, y1, x2, y2 = (int(v) for v in item["bbox_xyxy_pixels"])
                    label = f'{item["class_name"]} {item["confidence"]:.2f}'
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, max(20, y1 - 8)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
                cv2.putText(frame, "MODEL OUTPUT - NOT SAFETY VALIDATED", (8, 24),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 1)
            else:
                cv2.putText(frame, "CAMERA PREVIEW ONLY - NO AI DETECTION", (8, 24),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 1)
            cv2.imshow("PUI89 Coconut Harvest AI - Local Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

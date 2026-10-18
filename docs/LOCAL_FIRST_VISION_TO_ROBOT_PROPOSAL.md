# Local-First Vision-to-Robot Proposal

This implementation adds an optional local path from an RGB image and aligned depth map to a reviewable coconut-target proposal.

## Cost and network behavior

- No hosted inference APIs, cloud resource creation, or model downloads are used by this script.
- You must supply an existing local `.pt` or `.pth` model whose class list includes a class exactly named `coconut`.
- Ultralytics is optional and must be installed by you if you choose to use a compatible local model. The script does not install dependencies.
- Depth is read from a local NumPy `.npy` file. Images, depth maps, and reports are not uploaded by this module.
- Local inference can still use substantial CPU, RAM, disk, bandwidth (if you manually download weights), and electricity. Check model/data licences and file sizes.

## Inputs

1. An RGB image.
2. A numeric 2-D depth map aligned to that image.
3. Camera intrinsics JSON, for example:

```json
{
  "fx": 615.0,
  "fy": 615.0,
  "cx": 320.0,
  "cy": 240.0
}
```

4. A compatible local detector trained with a coconut class.

Use `--depth-scale 0.001` for raw depth values in millimetres; use `1.0` if values are already metres.

## Run locally

From the repository root, after you have chosen to install NumPy and Ultralytics and have a compatible local model:

```bash
python -m apps.pui89_app.local_first_pipeline \
  --weights ./models/coconut_detector.pt \
  --image ./data/orchard.jpg \
  --depth-npy ./data/aligned_depth.npy \
  --intrinsics-json ./data/camera_intrinsics.json \
  --depth-scale 0.001 \
  --output ./coconut_robot_proposal.json
```

Paths are examples, not bundled assets. The repository does not include detector weights; the command will not download them.

## What the report means

- Only predictions whose class name is exactly `coconut` are retained.
- Median depth near the bounding-box centre yields a camera-frame XYZ estimate, not a world-frame robot pose.
- Missing or invalid depth becomes `UNKNOWN`, not an invented coordinate.
- Confidence and range checks are software gates, not validated workspace or safety limits.
- Human approval records review only; it does not authorize robot motion.
- Every report sets `actuator_commands_authorized=false` and `robot_execution=NOT_IMPLEMENTED`.

This does not provide a robot-frame transform, reachability solver, full-volume collision checker, force/torque monitoring, emergency-stop hardware, or physical safety certification. Before any real robot test, validate sensor alignment/calibration, measure detector and localization performance on held-out orchard data, independently validate kinematics and collision checking, and complete a supervised safety review.

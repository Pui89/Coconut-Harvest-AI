# Local coconut detector training

This folder provides reproducible scripts; it does **not** contain a trained model or dataset. The scripts run locally and refuse model IDs/URLs so they do not silently download weights. No hosted inference, cloud GPU, paid notebook, or paid API is needed.

## Fastest free start on Windows

From a local clone of the repository, run:

~~~powershell
python -m pip install -r tools/requirements-data.txt
python tools/collect_commons_coconuts.py --out data/commons_candidates --limit 30
python tools/build_candidate_gallery.py --collection-dir data/commons_candidates
Start-Process (Resolve-Path data/commons_candidates/review_gallery.html)
~~~

This produces a candidate gallery and provenance CSV locally. It is deliberately a small first batch to limit download size and review effort. Verify licences and remove out-of-domain images before annotation. No collection is downloaded when you merely browse this repository.

## Dataset decision

I did not identify a verified, fully downloadable, suitably licensed, non-Roboflow orchard object-detection dataset that I can responsibly recommend as ready to train. Some public GitHub results are only dataset listings or annotation tools and do not include the images or a clear licence. Do not train on them until access and rights are confirmed.

Use one of these routes:
1. Collect orchard images yourself, with permission, and label every visible coconut using bounding boxes.
2. Ask a researcher or farm to share an image dataset and written permission/licence.
3. Reconsider a public dataset only after verifying image download, annotation quality, source, licence, and attribution requirements.

Do not put copyrighted or private images in this public repository unless you have permission. Keep the dataset local; do not commit images or weights to Git.

## Expected YOLO dataset layout

~~~text
dataset/
  images/
    train/
    val/
    test/
  labels/
    train/
    val/
    test/
  coconut.yaml
~~~

Every image must have a matching .txt label file; empty files are valid for images with no coconuts. Each annotation row contains:

~~~text
class_id x_center y_center width height
~~~

Coordinates are normalized to [0, 1]. For a single-class dataset, class ID must be 0. Keep the test split frozen until model choice and confidence threshold are chosen. Split by orchard/tree/video session rather than randomly splitting adjacent frames, to reduce leakage. Include negative images with no coconuts.

Example coconut.yaml (edit the path for your computer):

~~~yaml
path: C:/datasets/coconut
train: images/train
val: images/val
test: images/test
names:
  0: coconut
~~~

## Local setup

Use an isolated environment. Do not replace the system Python. The documented laptop has a 4 GB RTX 3050 GPU and 16 GB RAM; start small. Install a Python/PyTorch combination supported by the operating system, GPU driver, and chosen Ultralytics version.

~~~powershell
python -m venv .venv-coconut
.venv-coconut\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r apps/pui89_app/requirements-detector.txt
~~~

Manually obtain a compatible base checkpoint from a source you trust and save it locally. Review the checkpoint and framework licences before use, especially for commercial distribution. Do not put weights in Git. The script refuses model names such as yolov8n.pt; pass a real local path. Ultralytics licensing may impose obligations or require a separate commercial licence depending on how the software is used or distributed.

## Convert labels from the offline annotation tool

The repository includes [an offline browser annotator](../tools/coconut_annotator.html) and [a JSON-to-YOLO converter](../tools/convert_annotations_to_yolo.py). The annotator exports a JSON file; it does not upload images or automatically label them. Run the converter with paths to the JSON, the output directory, and the original image directory:

~~~powershell
python tools/convert_annotations_to_yolo.py --annotations "C:\\path\\to\\coconut-annotations.json" --output-dir "C:\\datasets\\coconut-converted" --images-dir "C:\\path\\to\\original-images"
~~~

It writes one YOLO text file per image under `labels/` and a conversion summary. You must manually arrange each image with its corresponding label in the `images/train|val|test` and `labels/train|val|test` folders described above. Do not use the same tree, video, or capture session across splits. Images without visible coconuts should have an empty label file and be retained only when they are genuinely negative examples. Review boxes for missed fruit, loose boxes, and inconsistent annotation policy.

## Check labels before training

Run this first from the repository root:

~~~powershell
python training/check_dataset.py --root "C:\datasets\coconut"
~~~

The checker validates image/label pairs, image readability, the single coconut class ID, and normalized bounding boxes. Fix every error before training.

## Train

~~~powershell
python training/train_detector.py --model "C:\models\your-local-base-checkpoint.pt" --data "C:\datasets\coconut\coconut.yaml" --epochs 50 --imgsz 512 --batch 1 --device 0
~~~

If CUDA runs out of memory, stop and rerun with a smaller image size (for example 416) or CPU. Do not rent a cloud GPU to bypass the limit. Training writes weights, plots, CSV logs, and training_summary.json under runs/coconut/train by default.

## Test once on held-out data

After training and freezing your model choice, run:

~~~powershell
python training/evaluate_detector.py --weights "runs\coconut\train\weights\best.pt" --data "C:\datasets\coconut\coconut.yaml" --imgsz 512 --batch 1 --device 0 --output "reports\coconut_test_report.json"
~~~

The evaluator uses the framework's test-split validation and saves a JSON summary plus plots/artifacts. Review precision, recall, mAP@0.5, mAP@0.5:0.95, confusion matrix, missed coconuts, false positives, and performance by lighting, distance, occlusion, and tree/session. Record exact dataset version, split, checkpoint, package versions, device, image size, confidence threshold, and latency. Do not tune against the test split; if you do, it becomes validation data and a new independent test set is needed.

A report is generated only when you run the script with real labelled data and weights. No accuracy values are pre-filled or promised.

## Connect detection to the existing workflow

Once you have trained weights, run the existing RGB-D bridge on a local RGB image, aligned depth array saved as .npy, and camera intrinsics JSON:

~~~powershell
python -m apps.pui89_app.local_first_pipeline --weights "runs\coconut\train\weights\best.pt" --image "C:\data\orchard\frame.jpg" --depth-npy "C:\data\orchard\depth_aligned.npy" --intrinsics-json "C:\data\orchard\camera_intrinsics.json" --output "reports\coconut_robot_proposal.json"
~~~

Intrinsics JSON shape:

~~~json
{"fx": 600.0, "fy": 600.0, "cx": 320.0, "cy": 240.0}
~~~

The values above are placeholders, **not calibration values**. Replace them with calibration from the actual camera. The depth map must be aligned to the RGB image; set depth-scale correctly for the sensor. The output is a review proposal only. The workflow cannot infer robot-base position, reachability, obstacle clearance, or safe motion from a bounding box alone. Without valid spatial evidence, candidates are rejected or held for review. No actuator commands are sent.

## Safety and claims

A good detection score does not prove accurate 3D localization, ripeness, safe motion, or physical harvesting. Validate RGB-depth alignment, camera-to-robot calibration, tracking stability, robot reachability, collision checking, emergency stops, and a supervised non-cutting test separately. Keep model/data licences and source attribution with published results.


## Create an experiment provenance manifest

Before training or evaluation, record the exact dataset configuration and environment. From the repository root, run:

~~~powershell
python training/create_experiment_manifest.py --data "C:\datasets\coconut\coconut.yaml" --experiment-id "coconut-baseline-v1" --output "reports\coconut-baseline-v1-manifest.json"
~~~

After training, create a second manifest that includes the exact checkpoint checksum:

~~~powershell
python training/create_experiment_manifest.py --data "C:\datasets\coconut\coconut.yaml" --weights "runs\coconut\train\weights\best.pt" --experiment-id "coconut-test-v1" --seed 42 --notes "Frozen held-out test; describe any deviations" --output "reports\coconut-test-v1-manifest.json"
~~~

Replace example paths and the seed with what you actually used; do not record a seed unless it was really set. The script is local-only and does not download files, train a model, evaluate a model, or change your system configuration. It records Git commit/working-tree status, package versions, Python/platform details, visible GPU information when PyTorch is installed, dataset YAML SHA-256, configured split paths and image counts, and optional checkpoint SHA-256. Inspect the JSON before sharing it because it contains local file paths and machine details. A manifest is not a benchmark result and does not prove that labels, image licences, or split independence are correct.

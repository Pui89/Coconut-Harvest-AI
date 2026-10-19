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

## Current dataset status — 19 October 2026

The first-pass annotations in `data/review_batch_2026-10-18/annotations_v0.1.json` are historical only. Candidates 0002 and 0004 have been removed from the active training candidate set because their labels have unresolved QA issues. **Do not train from v0.1.**

Two replacement images, candidates 0033 and 0034, have passed source-page/licence recording and file checksum verification, but they are not labelled or independently reviewed yet. The active training dataset remains blocked until replacement annotations, second-review approval, and a sufficiently large group-separated dataset are available. See [replacement-image review](../docs/REPLACEMENT_IMAGE_CANDIDATES_2026-10-19.md) and [dataset QA gate](../docs/DATASET_QA_GATE_2026-10-19.md).

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

## Build the reviewed dataset (recommended)

The repository now has a packaging script that creates YOLO labels, copies images into train/validation/test folders, records source/licence metadata, and assigns entire group_id groups to one split. It refuses to build unless every image has a human review record, the original-source provenance is present, and the reviewer marks the licence as checked. It does **not** check whether a human drew accurate boxes.

### 1. Create a review CSV

Open a spreadsheet and save `reviewed_images.csv` as UTF-8 CSV with these exact columns:

~~~csv
filename,review_status,group_id,license_verified
0001_example.jpg,reviewed_positive,tree_or_session_01,yes
0002_example.jpg,reviewed_negative,tree_or_session_02,yes
~~~

The example rows are format examples only; replace them with your real filenames and review decisions. Include one row for every image in the annotation JSON. Use `reviewed_positive` only when you labelled every clearly visible coconut; use `reviewed_negative` only after checking that the image contains no coconut target. Do not label hidden or ambiguous fruit by guessing. Set `license_verified` to `yes` only after checking the original source page and reuse conditions. Use a meaningful `group_id` for a tree, capture session, video, or known related-source group. Do not split frames from the same video/tree across train, validation and test.

### 2. Build the dataset from reviewed labels

For the Commons collector's output, the original images are under `data/commons_candidates/images` and provenance is `data/commons_candidates/provenance.csv`. Adjust the JSON path and filenames to match your local files:

~~~powershell
python training/build_dataset_from_annotations.py `
  --annotations "C:\datasets\coconut-annotations.json" `
  --images-dir "C:\path\to\commons_candidates\images" `
  --reviewed-csv "C:\datasets\reviewed_images.csv" `
  --provenance-csv "C:\path\to\commons_candidates\provenance.csv" `
  --output "C:\datasets\coconut-v1" `
  --seed "pui89-coconut-v1"
~~~

The output includes `images/train|val|test`, matching `labels/` directories, `coconut.yaml`, `dataset_manifest.csv`, and `dataset_build_summary.json`. The output directory must not already exist. The script needs at least three distinct groups; more independent groups are strongly preferred. If all your images are from one or two trees or sessions, collect more independent scenes rather than weakening the split rule.

### 3. Run both data audits

~~~powershell
python training/check_dataset.py --root "C:\datasets\coconut-v1"
python training/audit_dataset_splits.py --root "C:\datasets\coconut-v1" --output "C:\datasets\coconut-v1\split_audit.json"
~~~

Generate an offline visual label-review gallery before training:

~~~powershell
python tools/preview_yolo_labels.py --root "C:\datasets\coconut-v1" --split train --out "reports\coconut-label-qa-train"
Start-Process (Resolve-Path "reports\coconut-label-qa-train\index.html")
python tools/preview_yolo_labels.py --root "C:\datasets\coconut-v1" --split val --out "reports\coconut-label-qa-val"
Start-Process (Resolve-Path "reports\coconut-label-qa-val\index.html")
python tools/preview_yolo_labels.py --root "C:\datasets\coconut-v1" --split test --out "reports\coconut-label-qa-test"
Start-Process (Resolve-Path "reports\coconut-label-qa-test\index.html")
~~~

Review the manifest and visually inspect the image/box galleries before training. The builder checks file integrity and metadata consistency, not visual label correctness, true orchard representativeness, or licence compliance. A build summary is not a trained detector result.
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

## Run the local baseline pipeline (after dataset QA)

After the reviewed dataset builder succeeds, both dataset audits return success, and you have a compatible trusted local `.pt` base checkpoint, you can run the training and frozen-test sequence with one PowerShell command. This pipeline installs nothing and downloads neither a dataset nor weights.

From the repository root:

~~~powershell
powershell -ExecutionPolicy Bypass -File scripts/run_coconut_baseline.ps1 `
  -DatasetRoot "C:\datasets\coconut-v1" `
  -LocalCheckpoint "C:\models\your-local-base-checkpoint.pt" `
  -ExperimentId "coconut-baseline-v1" `
  -Epochs 30 `
  -ImageSize 416 `
  -Device 0
~~~

The script checks image/label structure and exact duplicate split leakage, records a pre-training manifest, trains with batch size 1, evaluates once on the test split, records checkpoint/data checksums, and audits report provenance. The 416-pixel setting and 30 epochs are a conservative starting point for a reported 4 GB RTX 3050, not a guarantee against out-of-memory errors or a promise of accuracy. If CUDA fails, stop and retry with `-ImageSize 320` or `-Device cpu`; do not rent cloud compute.

Generated files are local under `reports/` and `runs/coconut/<ExperimentId>/`. Read the test report and both audits; inspect missed coconuts and false positives before describing any metric. If the test split is used to change settings, it is no longer a frozen test set. A measured result is valid only after the pipeline actually finishes with real reviewed labels and a held-out test split.
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

## Audit report provenance

The detector evaluator records SHA-256 checksums for the exact dataset YAML and checkpoint it evaluates. After evaluation, generate a manifest for the same YAML and checkpoint, then cross-check them:

~~~powershell
python training/create_experiment_manifest.py --data "C:\datasets\coconut\coconut.yaml" --weights "runs\coconut\train\weights\best.pt" --experiment-id "coconut-test-v1" --output "reports\coconut-test-v1-manifest.json"
python training/audit_experiment_report.py --manifest "reports\coconut-test-v1-manifest.json" --report "reports\coconut_test_report.json" --output "reports\provenance_audit.json"
~~~

The audit exits with code 0 only when the test-report status/split, nonempty metrics, dataset YAML checksum, and checkpoint checksum are consistent. It exits non-zero if required evidence is missing or does not match. Run the evaluator after the checksum fields were added; older reports must be regenerated. This is a provenance consistency check, not proof of correct annotations, legal image reuse, independent data, or real-world performance. Review generated JSON files before sharing because they can contain local paths and machine details.

# Windows Quick Start: Coconut Image Annotation

This guide is for the first real-image annotation step. It is designed for Windows Command Prompt and uses the offline annotator; it does not require a paid service or model download.

## Option A — easiest: open the repository's launcher

1. Download the repository to your computer and extract the ZIP file.
2. Open the extracted `Coconut-Harvest-AI` folder in File Explorer. It should contain `README.md`, `tools`, and `OPEN_COCONUT_ANNOTATOR.bat`.
3. Double-click `OPEN_COCONUT_ANNOTATOR.bat`.
4. In the browser annotator, select image files that you have permission to review. Draw boxes only around individual coconuts that can be identified clearly.
5. Export the annotation JSON to a folder you can find again, such as Documents. Keep it outside the repository until labels and image rights are reviewed.

The annotator runs from a local HTML file and does not upload your selected images.

## Option B — use Command Prompt

First open the repository folder in File Explorer. Click the address bar, type `cmd`, and press Enter. This opens Command Prompt in the correct folder.

Check that you are in the repository root:

```bat
dir
```

The listing should include `README.md`, `tools`, and `OPEN_COCONUT_ANNOTATOR.bat`. Then run:

```bat
start "" "tools\coconut_annotator.html"
```

**Important:** a command such as `start tools\coconut_annotator.html` will fail if Command Prompt is currently in `C:\Users\user` rather than inside the repository folder. Do not guess the repository path; open Command Prompt from the folder as described above, or use Option A.

## After exporting annotations

Replace the example paths below with the actual location and filename of your export. These are commands, not files automatically supplied by the repository.

1. Run the geometry audit:

```bat
python tools\audit_coconut_annotations.py --annotations "C:\path\to\coconut-annotations.json" --output "C:\path\to\annotation-audit.json"
```

2. Inspect every image at full resolution and review the box overlays. A geometry pass only checks coordinates; it does not prove the boxes identify coconuts correctly.
3. Only after visual inspection and independent human label QA, convert the annotation JSON to evaluator-ready ground truth:

```bat
python tools\annotations_to_ground_truth_csv.py --annotations "C:\path\to\coconut-annotations.json" --output "C:\path\to\ground_truth.csv" --confirm-human-qa
```

If the image files are in a known folder, add `--images-dir "C:\path\to\images"` to require the referenced images to exist. Do not use `--confirm-human-qa` before that review actually happens.

## What this step does and does not prove

- It creates human annotations for later experiments.
- It does not train a model or run detector inference.
- It does not establish coconut-detection accuracy.
- It does not by itself approve the image licence for training or redistribution.
- Do not create prediction CSV rows by hand. Benchmark metrics require real predictions from a detector run on the same held-out images.

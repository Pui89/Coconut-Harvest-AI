# Build a free starter image collection

No personal photos are required to begin. This script queries Wikimedia Commons and downloads only images whose declared licence is CC0, Public Domain, CC BY, or CC BY-SA; it excludes licences marked non-commercial or no-derivatives. The script stores the file-page URL, author/credit, licence, and source query in `provenance.csv`.

## Run locally

~~~powershell
python -m pip install -r tools/requirements-data.txt
python tools/collect_commons_coconuts.py --limit 100
~~~

It saves candidate images under `data/commons_candidates/images/` and a licence/provenance manifest in the same folder. Review each file's original Commons page and its actual licence terms before using or redistributing it. The collector does not include any image in Git; the data folder should remain local.

## Important limitation

This is **not** an existing labelled dataset. Search results can include coconuts on beaches, in markets, or as close-ups, which are not representative of a harvesting robot looking upward into a palm canopy. Manually keep only useful images, annotate every visible coconut with bounding boxes, and record exclusions. Do not treat unreviewed images as training data.

For a first experiment, aim for three separate groups:
- Training: diverse orchard images from multiple trees/sessions.
- Validation: different trees or sessions for model selection.
- Test: different trees/sessions kept untouched until final evaluation.

If the collected set does not contain enough genuine canopy/orchard views, use it only to test the annotation/training pipeline, not to claim field-ready performance. The most valuable next step is obtaining permission to use a real orchard dataset from an agricultural research group.


## Offline annotation tool (added to the repository)

A small browser-based annotation tool is available at [tools/coconut_annotator.html](../tools/coconut_annotator.html). Download the HTML file from GitHub and open it in a modern browser (or open the file from a local checkout). It runs locally in the browser and does not upload images. Choose multiple image files, draw a box around each visible coconut, and export `coconut-annotations.json`. It is an annotation aid, not an automatic labeller; every box must be reviewed by a person.

Convert the exported annotations to YOLO label files from the repository root:

~~~powershell
python tools/convert_annotations_to_yolo.py --annotations "C:\\path\\to\\coconut-annotations.json" --output-dir "C:\\datasets\\coconut-converted" --images-dir "C:\\path\\to\\original-images"
~~~

The converter writes a `labels/` directory and `conversion_summary.json`. It does not copy images or create train/validation/test splits. Arrange images and matching labels into the documented YOLO folder layout, keep each image paired with its matching label file, and split by tree or capture session—not random adjacent frames. Inspect the converted labels and run `training/check_dataset.py` before training.

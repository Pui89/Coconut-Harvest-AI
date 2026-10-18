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

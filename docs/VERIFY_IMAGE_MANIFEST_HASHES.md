# Verify Actual Image Hashes Against the Dataset Manifest

This free, standard-library-only utility computes SHA-256 from each local image file and compares it with the declared manifest value. It also catches exact byte-identical files assigned to different splits. It does not install dependencies, download data, train a model, or make network calls.

## Run

From the repository root:

    python tools/verify_image_manifest_hashes.py path/to/manifest.csv --images-dir data/real_image_samples --output image-hash-verification.json

The CSV must contain:

    image_id,filename,split,group_id,sha256

Each filename must be relative to the images directory and remain inside that directory. The command returns exit code 0 only when every listed file exists, all hashes match, and no exact-byte duplicate appears across splits. It returns a nonzero code when verification finds an issue.

## What this proves—and does not prove

- Reported actual SHA-256 values are computed from local file bytes at verification time.
- A matching digest supports file identity, not image rights or label quality.
- Exact-byte duplicates across splits are flagged even if the manifest declared different hashes.
- Resized images, crops, and near-duplicates are not detected.
- Continue to use the dataset split leakage audit to check declared group IDs across splits.
- A successful check is dataset-integrity evidence, not model-accuracy evidence.

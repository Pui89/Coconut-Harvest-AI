# Automatic Coconut Image Candidate Fetcher

This free, standard-library-only utility retrieves current Wikimedia Commons metadata for the project's fixed five-image allowlist. With `--download`, it downloads the original files to a local review folder and records source-page URL, creator metadata, licence fields, dimensions, byte size, and SHA-256.

## From the repository root (Windows)

First inspect current source metadata without downloading images:

```bat
python tools\fetch_coconut_candidates.py
```

Then download the allowlisted candidates for local review:

```bat
python tools\fetch_coconut_candidates.py --download
```

Expected output folder: `data\candidate_images\`

Manifest: `data\candidate_images\source_manifest.json`

To choose a different local output folder:

```bat
python tools\fetch_coconut_candidates.py --download --output-dir data\candidate_images
```

## What this automates

- Queries Commons for current file metadata rather than relying only on a static shortlist.
- Downloads only the fixed allowlist of five file pages (not arbitrary user-supplied URLs).
- Computes SHA-256 for each downloaded file.
- Records failures per candidate and continues with the remaining candidates.
- Writes a JSON provenance manifest.

## What it deliberately does not automate

- It does not determine whether a licence is legally suitable for a particular use. Verify each file page, attribution, licence version, and redistribution obligations.
- It does not inspect image contents, annotate coconuts, verify labels, or perform independent human QA.
- It does not promote any image into the training set. Every record is explicitly marked `training_approved: false`.
- It does not train a model or claim detector performance.

Review the original files and manifest, annotate at native resolution, inspect every overlay, and complete independent QA before changing the promotion ledger. Keep images from the same source/capture group together when splitting data. The image files are downloaded locally and are not automatically committed to GitHub.

## Network and cost

The script uses Wikimedia Commons over HTTPS and Python's standard library. It requires an internet connection but no account, paid API, model weights, or additional Python package. Respect Wikimedia's service terms and avoid repeated unnecessary runs.

# PUI89 Coconut Harvest AI — Real-Image Evidence Automation

**Status:** implemented on a feature branch; workflow execution and collected results are pending.
**Purpose:** make candidate-image collection and evidence preparation repeatable without treating public images as a labelled or approved dataset.

## What is automated

Run the GitHub Actions workflow **Collect Real Coconut Image Evidence Batch** manually. It accepts a bounded candidate limit (1–100) and per-image size limit (0.1–12 MB), then:

1. Queries Wikimedia Commons using the existing collector.
2. Downloads candidates whose declared licence metadata passes the collector's preliminary allow-list (CC0, Public Domain, CC BY or CC BY-SA; NC/ND excluded).
3. Records source-page URL, declared licence, creator/credit and search query.
4. Builds a local HTML review gallery.
5. Calculates SHA-256 for each downloaded file.
6. Creates a human-review CSV separating rights, visual relevance, tree-attached context, appearance class, biological maturity and target-product suitability.
7. Uploads the batch as a temporary workflow artifact with 7-day retention. Candidate images are not committed to Git.

## What is deliberately not automated

Automation cannot independently establish whether a displayed licence is valid for a particular image and intended commercial or derivative use; whether the image is a useful orchard/canopy view; biological maturity from colour alone; internal meat thickness, water quality, embryo status or seed viability; correctness of boxes and labels; or suitability for training.

Every image starts as UNREVIEWED and training_approved is always false. Human rights review and independent annotation QA remain mandatory. The workflow does not train a model, download model weights, calculate model accuracy, or perform robot/actuator actions.

## Product-purpose labels

Keep three annotation layers separate:

1. Appearance class: young_green, mature_green, yellow, brown_aging, or uncertain.
2. Biological/harvest evidence: maturity measurements or qualified agronomic assessment, harvest timing and uncertainty. An exterior image alone may not establish internal kernel thickness, water quality, embryo status or seed viability.
3. Target-product suitability: fresh_drinking, soft_meat, coconut_milk, copra, coconut_oil, seed_nut, germinated_coconut, other or unknown. This requires appropriate ground-truth observations or qualified review, not colour alone.

One fruit may have multiple potential uses. Preserve multi-purpose suitability as separate reviewed records or a documented multi-label field; do not force one exclusive destination.

## After downloading the artifact

1. Open review_gallery.html and inspect every image at full resolution.
2. Verify the source page, creator, licence, attribution and commercial/derivative conditions.
3. Exclude or mark unsuitable duplicate, market-only, beach, cut-open or non-canopy images as challenge-only where appropriate.
4. Record orchard/tree/session/source grouping; do not randomly split adjacent frames.
5. Annotate each visible fruit individually and preserve uncertain/occluded cases for review.
6. Obtain independent human review; use a qualified coconut agronomist for biological maturity and product-use adjudication.
7. Update canonical rights and review ledgers only from actual review outcomes, then run the fail-closed promotion gate and split-leakage audit.
8. Train/evaluate only after all gates pass, using a frozen group-separated test set and approved local CPU-compatible tools.

## Cost, privacy and evidence boundaries

- Manual-only trigger: no schedule or push trigger downloads images.
- Uses the existing collector and data dependency; no hosted AI API, cloud GPU, paid model or model-weight download.
- Candidate images are stored in a temporary GitHub Actions artifact for 7 days, not committed to Git. Do not upload private orchard/customer images to this workflow.
- GitHub-hosted runner and artifact availability are subject to GitHub service policies; no external service fee is asserted.
- A successful workflow means candidate collection and evidence preparation completed. It is not licence approval, a labelled dataset, model result, maturity validation or harvesting capability.

## Reproduction

    python tools/collect_commons_coconuts.py --out data/commons_candidates --limit 30 --max-mb 12
    python tools/build_candidate_gallery.py --collection-dir data/commons_candidates
    python tools/prepare_coconut_review_batch.py --collection-dir data/commons_candidates --output-dir reports/coconut-real-image-batch

Run the standard-library unit tests:

    python -m unittest tests.test_prepare_coconut_review_batch -v

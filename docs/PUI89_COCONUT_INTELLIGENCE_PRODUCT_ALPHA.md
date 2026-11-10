# PUI89 Coconut Intelligence — Product Alpha

**Status:** Expanded internal alpha. Automated tests cover the record service; the Streamlit interface still requires a manual walkthrough. No customer pilot, field validation, commercial release, or model-accuracy claim is made.

## Current operator workflow
1. Create a batch of up to 10 JPEG, PNG or WebP images (10 MB each; 50 MB batch total).
2. Record source/provenance and confirm authority to use and store every selected image.
3. Preserve original image bytes locally with SHA-256 hashes and a shared batch identifier.
4. Review deterministic image-screening indicators: image dimensions, grayscale brightness, contrast, approximate clipping and edge-strength proxy.
5. Record human visibility and occlusion review as append-only revisions.
6. Adjust a normalised bounding box and preview it over the unchanged image before saving a human annotation.
7. Use four visual appearance labels or UNKNOWN / NEEDS REVIEW.
8. Export a JSON report, bilingual English/Thai Markdown report, or verified annotation manifest.

## Run locally
Use an existing Python environment where Streamlit and Pillow are already available. Do not install packages without reviewing costs, licence and hardware.

~~~bash
streamlit run apps/pui89_app/inspection_app.py
python -m unittest apps.pui89_app.test_inspection_workspace -v
~~~

Default workspace: ~/.pui89/coconut-inspections. Set PUI89_COCONUT_WORKSPACE to choose another local folder. Keep this workspace outside Git and back it up independently.

## Image-quality indicators: important limits
- Brightness, contrast, clipping and edge strength are deterministic screening heuristics, not a validated quality score, focus detector, visibility classifier or training-eligibility decision.
- Human visibility/occlusion review is recorded separately from machine-computed indicators.
- A green/clear indicator does not prove that a photo is suitable for model training.

## Annotation and dataset governance
- The bounding-box UI provides coordinate sliders and an image overlay preview; it is not drag-and-drop drawing.
- The annotation manifest includes hashes, site/batch grouping, labels and boxes. It does not include image bytes.
- Training is NOT APPROVED BY DEFAULT. Human labels need adjudication.
- Split by orchard/site, tree, capture session and near-duplicate group before model evaluation. Do not randomly split correlated images across train/validation/test.
- No automatic train/validation/test split or model performance is claimed.

## Boundaries
- No automatic maturity classification is performed by this workspace.
- Labels are human-entered visual annotations, not botanical maturity certification.
- No yield, height, reachability, harvest-readiness or robot-safety claim.
- No physical actuator commands, hosted inference or automatic cloud upload.
- The product alpha is not a validated customer product.

## Verification and next gates
- CI unit tests use synthetic bytes; they do not test real image decoding, the Streamlit UI or field performance.
- Manually walk through multiple photos, quality review, box preview, reports and manifest export on the target computer.
- Verify local backup and full restore before collecting sensitive farm data.
- Use rights-cleared photos and document consent/privacy/retention with pilot partners.
- Only enable model training after a reviewed, rights-cleared dataset and group-separated independent evaluation are ready.

# PUI89 Coconut Intelligence — Product Alpha

**Release target:** Local-first inspection workspace alpha.  
**Status:** Implemented software increment; not yet independently tested, field validated, or commercially released.

## Operator workflow
1. Create an inspection using a JPEG, PNG or WebP photo (maximum 10 MB).
2. Record the source and confirm authority to use/store the image.
3. Keep the original image in a local workspace and verify its SHA-256 on export.
4. Record site code, operator alias and notes.
5. Add fruit annotations with normalised bounding boxes and one of four visual appearance classes, or UNKNOWN / NEEDS REVIEW.
6. Append annotations as new revisions; previous events remain in the local JSONL audit history.
7. Export a JSON report with provenance, annotation history, integrity result and limitations.

## Run locally
Use an existing Python environment where Streamlit and Pillow are already available. Do not install packages without reviewing costs, licence and hardware.

~~~bash
streamlit run apps/pui89_app/inspection_app.py
~~~

Default workspace: ~/.pui89/coconut-inspections

Set PUI89_COCONUT_WORKSPACE to choose another local folder. Keep this workspace outside Git and back it up independently.

## Boundaries
- No automatic image classification is performed.
- Labels are human-entered visual annotations, not botanical maturity certification.
- Bounding boxes are manually entered coordinates; interactive drawing is not included in this alpha.
- No yield, height, reachability, harvest-readiness or robot-safety claim.
- No physical actuator commands.
- Images stay local; no automatic cloud upload or hosted inference.

## Test
~~~bash
python -m unittest apps.pui89_app.test_inspection_workspace -v
~~~

Tests use synthetic bytes only and do not establish image-decoder correctness or field performance.

## Before an external pilot
- Run unit tests and manual usability walkthrough.
- Verify upload limits and backup/restore on target computer.
- Review privacy and retention terms with each pilot partner.
- Use images with documented rights and consent where required.
- Add interactive box drawing and multi-reviewer adjudication based on operator feedback.
- Keep classifier disabled until real, rights-cleared, independently split data and evaluation results exist.

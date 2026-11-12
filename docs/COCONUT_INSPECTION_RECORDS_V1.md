# Coconut Inspection Records v1 — implementation slice

**Status:** implemented on a feature branch and connected to a local-first Streamlit inspection screen. Not yet merged. This is an early software increment, not a complete customer-ready application.

## What is included

The standard Python module `apps/pui89_app/inspection_records.py` provides:

- local inspection creation, listing and reopening;
- image import into the selected workspace, with supported-format decoding, size/pixel limits and SHA-256 integrity records;
- image-source metadata and an explicit rights-status field (default: `unverified`);
- human assessment labels: the canonical four visual categories `young_green`, `mature_green`, `yellow`, and `brown_aging`, plus `unknown` and `review`;
- historical `developing_green` values remain readable in existing records but are not accepted for new annotations or silently converted;
- optional normalized bounding boxes with strict boundary checks;
- append-only assessment revisions with reviewer alias, timestamp, reason and confidence origin;
- JSON report generation with current assessments, revision history, evidence counts and limitations.

The module uses the existing Python application environment and Pillow, which is already part of the Streamlit dependency stack. It adds no package, hosted API, model download, database server or workflow.

## Local usage

Run from the repository root:

```python
from apps.pui89_app.inspection_records import InspectionRecordStore

store = InspectionRecordStore("./local-inspection-workspace")
inspection = store.create_inspection(
    operator_alias="operator-01",
    site_code="farm-A",
    notes="Morning inspection",
)
image = store.import_image(
    inspection["inspection_id"],
    image_bytes,  # bytes read from a user-selected local image
    filename="orchard.jpg",
    source_type="user_provided",
    source_reference="field notebook entry 01",
    rights_status="unverified",
)
store.add_annotation(
    inspection["inspection_id"],
    candidate_id="fruit-01",
    image_sha256=image["sha256"],
    maturity_label="yellow",
    reviewer_alias="reviewer-01",
    reason="Human visual assessment",
    bbox_xywh_normalized=[0.1, 0.2, 0.3, 0.4],
)
report_path = store.write_report(inspection["inspection_id"])
print(report_path)
```

The workspace is local to the path supplied by the operator. Image bytes are copied without transformation into an inspection-specific `images/` directory. JSON records and exports are written atomically. Keep the workspace in a location with appropriate local access controls and backups. Do not commit private farm images or inspection records to Git.

## Test

```powershell
python -m unittest apps.pui89_app.test_inspection_records -v
```

The tests use generated synthetic PNG bytes and temporary directories. They do not use real orchard data, validate maturity accuracy, test a deployed UI, or establish commercial readiness.

## Known gaps before MVP completion

- The Streamlit UI now creates/reopens records, imports images, records human labels and optional normalized boxes, shows revision history, and exports JSON. The UI has not yet had a full manual usability walkthrough.
- The existing offline drawing annotator is not yet embedded; this screen currently accepts optional normalized box coordinates as manual inputs.
- The report is JSON only; a designed operator-facing printable report remains future work.
- The record store is single-user/local-workspace oriented; concurrent multi-user writes and encrypted storage are not implemented.
- Rights status is recorded as supplied; it is not legal verification or permission to train.
- The module does not independently verify human label correctness or model calibration.
- Offline operation must still be tested end-to-end in the integrated application.
- No detector, autonomous decision, robot command, physical safety claim, customer pilot or commercial release is included.

This implementation is one bounded engineering increment toward MVP-01 to MVP-10. Do not mark all MVP criteria complete based on this module alone.

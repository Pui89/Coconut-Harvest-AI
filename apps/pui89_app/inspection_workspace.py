"""Local-first, append-only inspection records for PUI89 Coconut Intelligence."""
from __future__ import annotations
import hashlib, json, os, re, uuid
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = "pui89.coconut-inspection.v1"
LABELS = ("young", "developing_green", "mature_green", "brown_aging", "unknown_needs_review")
MAX_IMAGE_BYTES = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
SAFE_ID = re.compile(r"^[a-f0-9]{32}$")

class InspectionError(ValueError):
    pass

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def _safe_text(value, field, limit=500):
    if not isinstance(value, str):
        raise InspectionError(f"{field} must be text")
    value = value.strip()
    if len(value) > limit:
        raise InspectionError(f"{field} exceeds {limit} characters")
    return value

def _inspection_dir(workspace, inspection_id):
    if not SAFE_ID.fullmatch(inspection_id):
        raise InspectionError("invalid inspection ID")
    root = Path(workspace).expanduser().resolve()
    target = (root / "inspections" / inspection_id).resolve()
    if root not in target.parents:
        raise InspectionError("workspace path escape rejected")
    return target

def list_inspections(workspace):
    root = Path(workspace).expanduser().resolve() / "inspections"
    if not root.exists():
        return []
    result = []
    for folder in root.iterdir():
        if folder.is_dir() and SAFE_ID.fullmatch(folder.name):
            try:
                result.append(load_inspection(workspace, folder.name))
            except (OSError, ValueError, json.JSONDecodeError):
                continue
    return sorted(result, key=lambda item: item["created_at"], reverse=True)

def create_inspection(workspace, *, image_bytes, image_extension, image_format,
                      image_width, image_height, original_filename,
                      source_description, rights_confirmed, site_code="",
                      operator_alias="", notes=""):
    if not isinstance(image_bytes, bytes) or not image_bytes:
        raise InspectionError("image is empty")
    if len(image_bytes) > MAX_IMAGE_BYTES:
        raise InspectionError("image exceeds 10 MB limit")
    extension = image_extension.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise InspectionError("unsupported image extension")
    if image_format.upper() not in {"JPEG", "PNG", "WEBP"}:
        raise InspectionError("unsupported decoded image format")
    if not isinstance(image_width, int) or not isinstance(image_height, int) or min(image_width, image_height) < 1:
        raise InspectionError("invalid image dimensions")
    if not rights_confirmed:
        raise InspectionError("confirm that you are authorised to use this image")
    source_description = _safe_text(source_description, "source_description", 1000)
    if not source_description:
        raise InspectionError("source/provenance description is required")
    site_code = _safe_text(site_code, "site_code", 100)
    operator_alias = _safe_text(operator_alias, "operator_alias", 100)
    notes = _safe_text(notes, "notes", 2000)
    original_filename = Path(original_filename).name[:160] or "uploaded-image"
    root = Path(workspace).expanduser().resolve()
    inspection_id = uuid.uuid4().hex
    folder = _inspection_dir(root, inspection_id)
    images = folder / "images"
    images.mkdir(parents=True, exist_ok=False)
    digest = sha256_bytes(image_bytes)
    stored_image = images / f"{digest}{extension}"
    stored_image.write_bytes(image_bytes)
    event = {
        "event_type": "INSPECTION_CREATED", "revision": 1, "timestamp": utc_now(),
        "inspection_id": inspection_id, "schema_version": SCHEMA_VERSION,
        "site_code": site_code, "operator_alias": operator_alias, "notes": notes,
        "image": {"stored_filename": stored_image.name, "original_filename": original_filename,
                  "sha256": digest, "byte_size": len(image_bytes), "format": image_format.upper(),
                  "width": image_width, "height": image_height,
                  "source_description": source_description, "rights_confirmed_by_operator": True},
        "image_quality": {"visibility": "not_assessed", "occlusion": "not_assessed", "quality": "not_assessed"},
        "annotations": [],
        "limitations": ["No automatic image classification was performed.",
                        "Human-entered labels are not verified botanical maturity.",
                        "No harvest, yield, height, reachability, or robot-safety conclusion is provided."]
    }
    (folder / "events.jsonl").write_text(json.dumps(event, ensure_ascii=False) + "\n", encoding="utf-8")
    return event

def load_inspection(workspace, inspection_id):
    event_path = _inspection_dir(workspace, inspection_id) / "events.jsonl"
    if not event_path.is_file():
        raise InspectionError("inspection not found")
    current, expected_revision = None, 1
    with event_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            event = json.loads(line)
            if event.get("inspection_id") != inspection_id or event.get("revision") != expected_revision:
                raise InspectionError(f"invalid event history at line {line_number}")
            if current is None:
                if event.get("event_type") != "INSPECTION_CREATED":
                    raise InspectionError("first event must create inspection")
                current = event
            else:
                if event.get("event_type") != "ANNOTATION_ADDED":
                    raise InspectionError("unsupported event type")
                current = {**current, "annotations": current["annotations"] + [event["annotation"]],
                           "revision": event["revision"], "updated_at": event["timestamp"]}
            expected_revision += 1
    if current is None:
        raise InspectionError("empty inspection history")
    return current

def add_annotation(workspace, inspection_id, *, candidate_id, label, reviewer_alias,
                   x1, y1, x2, y2, reason=""):
    record = load_inspection(workspace, inspection_id)
    candidate_id = _safe_text(candidate_id, "candidate_id", 80)
    reviewer_alias = _safe_text(reviewer_alias, "reviewer_alias", 100)
    reason = _safe_text(reason, "reason", 1000)
    if not candidate_id or not reviewer_alias:
        raise InspectionError("candidate ID and reviewer alias are required")
    if label not in LABELS:
        raise InspectionError("unsupported maturity label")
    coords = (x1, y1, x2, y2)
    if any(not isinstance(v, (int, float)) for v in coords):
        raise InspectionError("bounding box coordinates must be numeric")
    if not (0 <= x1 < x2 <= 1 and 0 <= y1 < y2 <= 1):
        raise InspectionError("bounding box must satisfy 0 <= x1 < x2 <= 1 and 0 <= y1 < y2 <= 1")
    if any(a["candidate_id"] == candidate_id for a in record["annotations"]):
        raise InspectionError("candidate ID already exists; use a new ID for a new annotation")
    annotation = {"candidate_id": candidate_id, "label": label, "label_origin": "human",
                  "reviewer_alias": reviewer_alias, "reviewed_at": utc_now(),
                  "bbox_normalized_xyxy": [float(x1), float(y1), float(x2), float(y2)],
                  "reason_for_uncertainty": reason,
                  "status": "NEEDS_REVIEW" if label == "unknown_needs_review" else "HUMAN_ANNOTATION"}
    event = {"event_type": "ANNOTATION_ADDED", "revision": record["revision"] + 1,
             "timestamp": utc_now(), "inspection_id": inspection_id, "annotation": annotation}
    with (_inspection_dir(workspace, inspection_id) / "events.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    return load_inspection(workspace, inspection_id)

def export_report(workspace, inspection_id):
    record = load_inspection(workspace, inspection_id)
    image_path = _inspection_dir(workspace, inspection_id) / "images" / record["image"]["stored_filename"]
    if not image_path.is_file() or sha256_bytes(image_path.read_bytes()) != record["image"]["sha256"]:
        raise InspectionError("stored image integrity check failed")
    return {"report_type": "PUI89_COCONUT_INSPECTION", "report_version": "1.0",
            "exported_at": utc_now(), "record": record,
            "integrity": {"image_sha256_verified": True},
            "decision_boundary": {"automatic_classification_performed": False,
                                  "human_review_required": True, "harvest_authorized": False,
                                  "actuator_commands_sent": False}}

def image_path_for(workspace, inspection_id):
    record = load_inspection(workspace, inspection_id)
    path = _inspection_dir(workspace, inspection_id) / "images" / record["image"]["stored_filename"]
    if not path.is_file():
        raise InspectionError("stored image is missing")
    return path

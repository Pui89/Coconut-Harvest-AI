"""Local-first, human-led inspection records for Coconut Harvest AI.

This module stores inspection data on the operator-selected local workspace.
It performs no network requests, model inference, or physical actuation.
Image validation uses Pillow (already brought in by the Streamlit app stack).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import uuid
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from typing import Any

from PIL import Image, UnidentifiedImageError

SCHEMA_VERSION = "pui89-coconut-inspection-v1"
MATURITY_LABELS = {
    "young_green",
    "mature_green",
    "yellow",
    "brown_aging",
    "unknown",
    "review",
}
# Kept for reading and displaying pre-taxonomy-alignment records only.
# New annotations must use MATURITY_LABELS; legacy values are never auto-remapped.
LEGACY_MATURITY_LABELS = {"developing_green"}
CONFIDENCE_ORIGINS = {"human", "model", "not_provided"}
SUPPORTED_FORMATS = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp"}
MAX_IMAGE_BYTES = 20 * 1024 * 1024
MAX_IMAGE_PIXELS = 80_000_000
_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
_SHA_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class InspectionError(ValueError):
    """A safe, user-correctable inspection-record validation error."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _clean_text(value: Any, field: str, limit: int, *, required: bool = False) -> str:
    if value is None:
        value = ""
    if not isinstance(value, str):
        raise InspectionError(f"{field.upper()}_MUST_BE_TEXT")
    value = value.strip()
    if required and not value:
        raise InspectionError(f"{field.upper()}_REQUIRED")
    if len(value) > limit:
        raise InspectionError(f"{field.upper()}_TOO_LONG")
    if any(ord(char) < 32 and char not in "\t\n\r" for char in value):
        raise InspectionError(f"{field.upper()}_CONTAINS_CONTROL_CHARACTER")
    return value


def _validate_id(value: str, field: str) -> str:
    if not isinstance(value, str) or not _ID_PATTERN.fullmatch(value):
        raise InspectionError(f"{field.upper()}_INVALID")
    return value


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=".record-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except OSError:
            pass
        raise


class InspectionRecordStore:
    """Manage versioned inspection records and immutable image evidence locally."""

    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace).expanduser().resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.records_dir = self.workspace / "inspections"
        self.records_dir.mkdir(parents=True, exist_ok=True)

    def _record_path(self, inspection_id: str) -> Path:
        safe_id = _validate_id(inspection_id, "inspection_id")
        path = (self.records_dir / safe_id / "record.json").resolve()
        if self.records_dir.resolve() not in path.parents:
            raise InspectionError("INSPECTION_PATH_INVALID")
        return path

    def _read(self, inspection_id: str) -> dict[str, Any]:
        path = self._record_path(inspection_id)
        if not path.is_file():
            raise InspectionError("INSPECTION_NOT_FOUND")
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise InspectionError("INSPECTION_RECORD_UNREADABLE") from exc
        if not isinstance(record, dict) or record.get("schema_version") != SCHEMA_VERSION:
            raise InspectionError("INSPECTION_SCHEMA_UNSUPPORTED")
        return record

    def _save(self, record: dict[str, Any]) -> None:
        _atomic_json(self._record_path(record["inspection_id"]), record)

    def create_inspection(
        self,
        *,
        operator_alias: str,
        site_code: str = "",
        notes: str = "",
        inspection_id: str | None = None,
        created_at: str | None = None,
    ) -> dict[str, Any]:
        alias = _clean_text(operator_alias, "operator_alias", 80, required=True)
        site = _clean_text(site_code, "site_code", 80)
        note_text = _clean_text(notes, "notes", 2000)
        record_id = inspection_id or f"insp_{uuid.uuid4().hex}"
        _validate_id(record_id, "inspection_id")
        path = self._record_path(record_id)
        if path.exists():
            raise InspectionError("INSPECTION_ALREADY_EXISTS")
        timestamp = created_at or _utc_now()
        record = {
            "schema_version": SCHEMA_VERSION,
            "inspection_id": record_id,
            "status": "open",
            "created_at": timestamp,
            "updated_at": timestamp,
            "metadata": {
                "operator_alias": alias,
                "site_code": site,
                "notes": note_text,
            },
            "images": [],
            "candidates": [],
            "audit_events": [{
                "event": "inspection_created",
                "at": timestamp,
                "actor_alias": alias,
            }],
            "limitations": [
                "Human-led recordkeeping only; no maturity detector is implied.",
                "Source and reuse rights must be independently verified.",
                "No robot command or physical actuation is available.",
            ],
        }
        self._save(record)
        return record

    def get_inspection(self, inspection_id: str) -> dict[str, Any]:
        """Return the persisted record, including every candidate revision."""
        return self._read(inspection_id)

    def list_inspections(self) -> list[dict[str, str]]:
        """Return a small index without exposing image bytes or annotation contents."""
        results: list[dict[str, str]] = []
        if not self.records_dir.exists():
            return results
        for path in sorted(self.records_dir.glob("*/record.json")):
            try:
                record = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(record, dict) and record.get("schema_version") == SCHEMA_VERSION:
                    results.append({
                        "inspection_id": str(record.get("inspection_id", "")),
                        "status": str(record.get("status", "")),
                        "created_at": str(record.get("created_at", "")),
                        "site_code": str(record.get("metadata", {}).get("site_code", "")),
                    })
            except (OSError, UnicodeError, json.JSONDecodeError, AttributeError):
                continue
        return results

    def import_image(
        self,
        inspection_id: str,
        image_bytes: bytes,
        *,
        filename: str,
        source_type: str = "user_provided",
        source_reference: str = "",
        rights_status: str = "unverified",
    ) -> dict[str, Any]:
        """Validate and copy image bytes into the local workspace; never upload them."""
        record = self._read(inspection_id)
        if not isinstance(image_bytes, bytes) or not image_bytes:
            raise InspectionError("IMAGE_EMPTY_OR_MISSING")
        if len(image_bytes) > MAX_IMAGE_BYTES:
            raise InspectionError("IMAGE_EXCEEDS_SIZE_LIMIT")
        safe_filename = _clean_text(Path(str(filename)).name, "filename", 255, required=True)
        if safe_filename in {".", ".."}:
            raise InspectionError("IMAGE_FILENAME_INVALID")
        source_kind = _clean_text(source_type, "source_type", 40, required=True).lower()
        source_ref = _clean_text(source_reference, "source_reference", 2048)
        rights = _clean_text(rights_status, "rights_status", 40, required=True).lower()
        if rights not in {"unverified", "pending_review", "cleared", "restricted", "unknown"}:
            raise InspectionError("RIGHTS_STATUS_INVALID")

        try:
            with Image.open(BytesIO(image_bytes)) as image:
                image_format = image.format
                width, height = image.size
                if image_format not in SUPPORTED_FORMATS:
                    raise InspectionError("IMAGE_FORMAT_UNSUPPORTED")
                if width <= 0 or height <= 0 or width * height > MAX_IMAGE_PIXELS:
                    raise InspectionError("IMAGE_DIMENSIONS_INVALID")
                image.verify()
            # Re-open after verify to force a full decoder load and reject truncated/corrupt data.
            with Image.open(BytesIO(image_bytes)) as image:
                image.load()
                if image.format != image_format or image.size != (width, height):
                    raise InspectionError("IMAGE_VALIDATION_INCONSISTENT")
        except InspectionError:
            raise
        except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as exc:
            raise InspectionError("IMAGE_UNREADABLE_OR_CORRUPT") from exc

        digest = hashlib.sha256(image_bytes).hexdigest()
        extension = SUPPORTED_FORMATS[image_format]
        image_dir = self._record_path(inspection_id).parent / "images"
        image_dir.mkdir(parents=True, exist_ok=True)
        image_path = image_dir / f"{digest}{extension}"
        if image_path.exists():
            if hashlib.sha256(image_path.read_bytes()).hexdigest() != digest:
                raise InspectionError("STORED_IMAGE_HASH_MISMATCH")
        else:
            # Exclusive creation avoids silently replacing an existing evidence file.
            try:
                with image_path.open("xb") as handle:
                    handle.write(image_bytes)
                    handle.flush()
                    os.fsync(handle.fileno())
            except FileExistsError:
                if hashlib.sha256(image_path.read_bytes()).hexdigest() != digest:
                    raise InspectionError("STORED_IMAGE_HASH_MISMATCH")

        existing = next((item for item in record["images"] if item["sha256"] == digest), None)
        if existing:
            return existing
        item = {
            "image_id": f"img_{digest[:16]}",
            "original_filename": safe_filename,
            "stored_path": f"images/{digest}{extension}",
            "sha256": digest,
            "byte_size": len(image_bytes),
            "format": image_format.lower(),
            "width": width,
            "height": height,
            "imported_at": _utc_now(),
            "source": {
                "type": source_kind,
                "reference": source_ref,
                "rights_status": rights,
            },
            "integrity": "sha256_recorded_and_image_decoded",
        }
        record["images"].append(item)
        record["updated_at"] = _utc_now()
        record["audit_events"].append({
            "event": "image_imported",
            "at": record["updated_at"],
            "actor_alias": record["metadata"]["operator_alias"],
            "image_sha256": digest,
        })
        self._save(record)
        return item

    def read_image(self, inspection_id: str, image_sha256: str) -> bytes:
        """Read one stored image after checking its recorded digest."""
        if not isinstance(image_sha256, str) or not _SHA_PATTERN.fullmatch(image_sha256):
            raise InspectionError("IMAGE_SHA256_INVALID")
        record = self._read(inspection_id)
        item = next((entry for entry in record["images"] if entry["sha256"] == image_sha256), None)
        if item is None:
            raise InspectionError("IMAGE_NOT_FOUND")
        inspection_dir = self._record_path(inspection_id).parent.resolve()
        image_path = (inspection_dir / item["stored_path"]).resolve()
        if inspection_dir not in image_path.parents or not image_path.is_file():
            raise InspectionError("STORED_IMAGE_MISSING_OR_PATH_INVALID")
        try:
            payload = image_path.read_bytes()
        except OSError as exc:
            raise InspectionError("STORED_IMAGE_UNREADABLE") from exc
        if hashlib.sha256(payload).hexdigest() != image_sha256:
            raise InspectionError("STORED_IMAGE_HASH_MISMATCH")
        return payload

    def add_annotation(
        self,
        inspection_id: str,
        *,
        candidate_id: str,
        image_sha256: str,
        maturity_label: str,
        reviewer_alias: str,
        reason: str = "",
        confidence: float | None = None,
        confidence_origin: str = "not_provided",
        bbox_xywh_normalized: list[float] | tuple[float, float, float, float] | None = None,
    ) -> dict[str, Any]:
        """Append a candidate assessment revision; prior revisions are never overwritten."""
        record = self._read(inspection_id)
        candidate_key = _validate_id(candidate_id, "candidate_id")
        if not isinstance(image_sha256, str) or not _SHA_PATTERN.fullmatch(image_sha256):
            raise InspectionError("IMAGE_SHA256_INVALID")
        image = next((item for item in record["images"] if item["sha256"] == image_sha256), None)
        if image is None:
            raise InspectionError("ANNOTATION_IMAGE_NOT_IN_INSPECTION")
        label = _clean_text(maturity_label, "maturity_label", 40, required=True).lower()
        if label not in MATURITY_LABELS:
            raise InspectionError("MATURITY_LABEL_INVALID")
        reviewer = _clean_text(reviewer_alias, "reviewer_alias", 80, required=True)
        reason_text = _clean_text(reason, "reason", 1000)
        origin = _clean_text(confidence_origin, "confidence_origin", 30, required=True).lower()
        if origin not in CONFIDENCE_ORIGINS:
            raise InspectionError("CONFIDENCE_ORIGIN_INVALID")
        if confidence is not None:
            if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
                raise InspectionError("CONFIDENCE_OUT_OF_RANGE")
            confidence = float(confidence)
            if origin == "not_provided":
                raise InspectionError("CONFIDENCE_ORIGIN_REQUIRED")
        elif origin != "not_provided":
            raise InspectionError("CONFIDENCE_VALUE_REQUIRED")

        bbox: list[float] | None = None
        if bbox_xywh_normalized is not None:
            if not isinstance(bbox_xywh_normalized, (list, tuple)) or len(bbox_xywh_normalized) != 4:
                raise InspectionError("BBOX_INVALID")
            if any(isinstance(v, bool) or not isinstance(v, (int, float)) for v in bbox_xywh_normalized):
                raise InspectionError("BBOX_INVALID")
            x, y, width, height = (float(v) for v in bbox_xywh_normalized)
            if not (0 <= x < 1 and 0 <= y < 1 and 0 < width <= 1 and 0 < height <= 1
                    and x + width <= 1 and y + height <= 1):
                raise InspectionError("BBOX_OUT_OF_BOUNDS")
            bbox = [x, y, width, height]

        candidate = next((item for item in record["candidates"] if item["candidate_id"] == candidate_key), None)
        if candidate is None:
            candidate = {
                "candidate_id": candidate_key,
                "image_sha256": image_sha256,
                "revisions": [],
            }
            record["candidates"].append(candidate)
        elif candidate["image_sha256"] != image_sha256:
            raise InspectionError("CANDIDATE_IMAGE_CANNOT_CHANGE")

        revision = {
            "revision": len(candidate["revisions"]) + 1,
            "revision_id": f"rev_{uuid.uuid4().hex}",
            "supersedes": candidate["revisions"][-1]["revision_id"] if candidate["revisions"] else None,
            "maturity_label": label,
            "reviewer_alias": reviewer,
            "reviewed_at": _utc_now(),
            "reason": reason_text,
            "confidence": confidence,
            "confidence_origin": origin,
            "bbox_xywh_normalized": bbox,
            "assessment_kind": "human_review" if origin in {"human", "not_provided"} else "model_proposal",
        }
        candidate["revisions"].append(revision)
        record["updated_at"] = revision["reviewed_at"]
        record["audit_events"].append({
            "event": "candidate_assessment_added",
            "at": revision["reviewed_at"],
            "actor_alias": reviewer,
            "candidate_id": candidate_key,
            "revision": revision["revision"],
            "maturity_label": label,
        })
        self._save(record)
        return revision

    def export_report(self, inspection_id: str) -> dict[str, Any]:
        """Build a deterministic, machine-readable snapshot of the full inspection history."""
        record = self._read(inspection_id)
        current_assessments = []
        for candidate in record["candidates"]:
            if candidate["revisions"]:
                current_assessments.append({
                    "candidate_id": candidate["candidate_id"],
                    "image_sha256": candidate["image_sha256"],
                    "current": candidate["revisions"][-1],
                    "revision_count": len(candidate["revisions"]),
                })
        return {
            "report_schema": "pui89-coconut-inspection-report-v1",
            "generated_at": _utc_now(),
            "inspection": record,
            "current_assessments": current_assessments,
            "evidence_summary": {
                "image_count": len(record["images"]),
                "candidate_count": len(record["candidates"]),
                "assessment_revision_count": sum(len(c["revisions"]) for c in record["candidates"]),
                "images_with_unverified_or_pending_rights": sum(
                    1 for item in record["images"]
                    if item["source"]["rights_status"] not in {"cleared"}
                ),
            },
            "limitations": [
                "A recorded rights status is operator-supplied metadata, not independent legal verification.",
                "Human labels are not independently verified ground truth.",
                "Model-origin confidence, if present, is not necessarily calibrated.",
                "This report does not establish detector accuracy, yield, safety, or commercial readiness.",
                "No physical robot action is requested or performed.",
            ],
        }

    def write_report(self, inspection_id: str) -> Path:
        """Write a JSON report inside this inspection's local exports directory."""
        report = self.export_report(inspection_id)
        export_dir = self._record_path(inspection_id).parent / "exports"
        export_path = export_dir / "inspection-report.json"
        _atomic_json(export_path, report)
        return export_path

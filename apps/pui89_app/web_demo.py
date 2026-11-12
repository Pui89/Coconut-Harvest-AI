"""Interactive Streamlit demo for Coconut Harvest AI decision support.

This is a transparent rule-based demonstration, not a trained image detector.
Uploaded images are displayed for context; they are not automatically analysed.
"""
from __future__ import annotations

import io
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from apps.pui89_app.local_detector import detect_coconuts, load_local_coconut_model


@st.cache_resource(show_spinner="Loading trusted local model...")
def _load_cached_local_model(model_path: str):
    return load_local_coconut_model(model_path)

st.set_page_config(page_title="Coconut Harvest AI Demo", page_icon="🥥", layout="wide")

st.title("🥥 Coconut Harvest AI")
st.subheader("Interactive application example")
st.caption("Simulation-first decision-support demo · No physical robot control")

st.warning(
    "This demo does not detect coconuts from pixels. The uploaded photo is for visual context only. "
    "The result is based on the evidence values you enter below and transparent example rules."
)

with st.sidebar:
    st.header("Sensor and scene checks")
    rgb_available = st.checkbox("RGB image available", value=True)
    depth_valid = st.checkbox("Depth data valid", value=True)
    timestamp_skew_ms = st.slider("RGB/depth timestamp difference (ms)", 0, 100, 8)
    st.divider()
    st.caption("Illustrative software thresholds only — not validated field limits.")

left, right = st.columns([1, 1], gap="large")
with left:
    st.header("1. Orchard image")
    upload = st.file_uploader("Upload a coconut-orchard photo (optional)", type=["png", "jpg", "jpeg", "webp"])
    if upload is not None:
        st.image(upload, caption="Uploaded reference photo — not automatically analysed", use_container_width=True)
    else:
        st.info("Upload a photo to display it here, or continue with the example inputs.")

with right:
    st.header("2. Candidate evidence")
    st.write("Adjust these values to see how the decision-support rules respond.")
    st.caption("Stage and confidence below are manually supplied example evidence. The uploaded photo is not automatically classified.")
    harvest_mode = st.selectbox(
        "What should the operator request?",
        options=["all_mature", "young_green", "mature_green", "mature_brown_or_dry", "selected_combination", "survey_only"],
        format_func=lambda mode: {
            "all_mature": "All mature coconuts (mature green + mature brown/dry)",
            "young_green": "Young green coconuts",
            "mature_green": "Mature green coconuts",
            "mature_brown_or_dry": "Mature brown/dry coconuts",
            "selected_combination": "A selected combination of stages",
            "survey_only": "Survey only — do not harvest",
        }[mode],
    )
    safe_stage_options = ["young_green", "mature_green", "mature_brown_or_dry"]
    selected_stages = (
        st.multiselect(
            "Stages allowed for this task",
            options=safe_stage_options,
            default=["mature_green", "mature_brown_or_dry"],
        )
        if harvest_mode == "selected_combination"
        else None
    )
    candidate_stage = st.selectbox(
        "Candidate stage (manual input; not AI-predicted)",
        options=[
            "young_green",
            "mature_green",
            "yellow",
            "mature_brown_or_dry",
            "uncertain_stage",
            "damaged_or_abnormal",
            "occluded_or_partial",
            "flower_or_infant",
        ],
        format_func=lambda stage: {
            "young_green": "Young green",
            "mature_green": "Mature green",
            "yellow": "Yellow — visual category; review only",
            "mature_brown_or_dry": "Mature brown/dry",
            "uncertain_stage": "Uncertain — review required",
            "damaged_or_abnormal": "Damaged/abnormal — review required",
            "occluded_or_partial": "Occluded/partial — review required",
            "flower_or_infant": "Flower/infant — do not harvest",
        }[stage],
        index=2,
    )
    target_id = st.text_input("Candidate ID", value="coconut-01", max_chars=80)
    ripeness = st.slider("Ripeness evidence score", 0.0, 1.0, 0.91, 0.01)
    localization = st.slider("Localization confidence", 0.0, 1.0, 0.94, 0.01)
    distance = st.slider("Estimated distance (m)", 0.0, 8.0, 2.1, 0.1)
    clearance = st.slider("Estimated obstacle clearance (m)", 0.0, 1.5, 0.45, 0.05)
    stable_frames = st.slider("Consecutive stable tracking frames", 0, 30, 12)


with st.expander("Optional: run a trusted local coconut detector", expanded=False):
    st.caption(
        "This optional feature runs a user-supplied model file locally on CPU or a compatible NVIDIA GPU. "
        "It does not download weights, call a hosted API, or control a robot."
    )
    local_model_path = os.environ.get("PUI89_COCONUT_MODEL_PATH", "").strip()
    if not local_model_path:
        st.info(
            "No local model is configured. Set the environment variable "
            "`PUI89_COCONUT_MODEL_PATH` to an existing trusted .pt weights file, "
            "then restart the app. The model must have a class explicitly labelled coconut."
        )
    elif not Path(local_model_path).expanduser().is_file():
        st.error(
            "The configured local model file was not found. Check "
            "`PUI89_COCONUT_MODEL_PATH`. No online fallback will be attempted."
        )
    elif upload is None:
        st.info("Upload an orchard photo above to run local inference.")
    else:
        inference_device = st.selectbox(
            "Inference device",
            options=["auto", "cuda", "cpu"],
            index=0,
            help="Auto uses the NVIDIA GPU when PyTorch CUDA is available; otherwise it uses CPU.",
        )
        inference_image_size = st.selectbox(
            "Model input size",
            options=[384, 512, 640],
            index=0,
            help="Fastest starting point for this 4 GB GPU laptop. If small or distant coconuts are missed, compare 512 and 640 using the same labelled images.",
        )
        detector_confidence = st.slider(
            "Detection confidence threshold", 0.05, 0.95, 0.25, 0.05,
            key="local_detector_confidence",
        )
        if st.button("Run local image detection", use_container_width=True):
            try:
                from PIL import Image, ImageDraw

                from time import perf_counter
                from apps.pui89_app.local_detector import resolve_inference_device
                resolved_device = resolve_inference_device(inference_device)
                device_label = "GPU" if resolved_device == "0" else "CPU"
                with st.spinner("Running local inference on " + device_label + "..."):
                    model, coconut_ids = _load_cached_local_model(local_model_path)
                    image = Image.open(io.BytesIO(upload.getvalue())).convert("RGB")
                    inference_started = perf_counter()
                    detections = detect_coconuts(
                        model, image, coconut_ids, confidence=detector_confidence,
                        image_size=inference_image_size, device=inference_device,
                    )
                    inference_seconds = perf_counter() - inference_started
                overlay = image.copy()
                draw = ImageDraw.Draw(overlay)
                for detection in detections:
                    x1, y1, x2, y2 = detection["bbox_xyxy_pixels"]
                    label = f'{detection["class_name"]} {detection["confidence"]:.2f}'
                    draw.rectangle((x1, y1, x2, y2), outline="lime", width=3)
                    draw.text((x1, max(0, y1 - 18)), label, fill="lime")
                st.image(overlay, caption="Local model predictions — not a robot command", use_container_width=True)
                report = {
                    "status": "INFERENCE_COMPLETED",
                    "model_file": Path(local_model_path).name,
                    "inference_device": "cuda:0" if resolved_device == "0" else "cpu",
                    "model_input_size": inference_image_size,
                    "inference_seconds_excluding_model_load": round(inference_seconds, 4),
                    "confidence_threshold": detector_confidence,
                    "image_width_pixels": image.width,
                    "image_height_pixels": image.height,
                    "detection_count": len(detections),
                    "detections": detections,
                    "actuator_commands_sent": False,
                    "limitations": [
                        "Predictions are not validated until evaluated against labelled held-out images.",
                        "A bounding box does not provide calibrated 3D location, ripeness, reachability, or collision safety.",
                        "A zero-detection result does not prove that the image contains no coconuts.",
                        "Only trusted local model files should be loaded.",
                    ],
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }
                st.json(report)
                st.download_button(
                    "Download local inference JSON",
                    data=json.dumps(report, indent=2),
                    file_name="coconut_local_detection_report.json",
                    mime="application/json",
                    use_container_width=True,
                )
            except Exception as exc:
                st.error(f"Local inference could not be completed: {type(exc).__name__}: {exc}")
                st.caption(
                    "Check the model file, its class labels, and the optional detector dependencies. "
                    "No network fallback or actuator command was attempted."
                )

if st.button("Analyse candidate", type="primary", use_container_width=True):
    sensor_reasons = []
    if not rgb_available:
        sensor_reasons.append("RGB_UNAVAILABLE")
    if not depth_valid:
        sensor_reasons.append("DEPTH_INVALID")
    if timestamp_skew_ms > 30:
        sensor_reasons.append("TIMESTAMP_SKEW_EXCEEDED")

    if sensor_reasons:
        result = {
            "status": "SAFE_HOLD",
            "harvest_mode": harvest_mode,
            "selected_stages": selected_stages,
            "sensor_reasons": sensor_reasons,
            "decisions": [],
            "actuator_commands_sent": False,
        }
    else:
        reasons = []
        mode_stage_map = {
            "all_mature": {"mature_green", "mature_brown_or_dry"},
            "young_green": {"young_green"},
            "mature_green": {"mature_green"},
            "mature_brown_or_dry": {"mature_brown_or_dry"},
        }
        allowed_stages = set(selected_stages or []) if harvest_mode == "selected_combination" else mode_stage_map.get(harvest_mode, set())
        if harvest_mode == "survey_only":
            reasons.append("SURVEY_ONLY_NO_HARVEST")
        elif candidate_stage in {"yellow", "uncertain_stage", "damaged_or_abnormal", "occluded_or_partial", "flower_or_infant"}:
            reasons.append("STAGE_REQUIRES_HUMAN_REVIEW_OR_PROTECTION")
        elif candidate_stage not in allowed_stages:
            reasons.append("STAGE_NOT_SELECTED_FOR_THIS_HARVEST_TASK")
        if harvest_mode == "selected_combination" and not allowed_stages:
            reasons.append("NO_HARVEST_STAGES_SELECTED")
        if localization < 0.80:
            reasons.append("LOCALIZATION_CONFIDENCE_LOW")
        if stable_frames < 5:
            reasons.append("TRACK_NOT_STABLE")
        if distance > 3.0:
            reasons.append("OUTSIDE_CONFIGURED_REACH")
        if clearance < 0.30:
            reasons.append("CLEARANCE_INSUFFICIENT")
        if ripeness < 0.65:
            reasons.append("RIPENESS_BELOW_CONFIGURED_THRESHOLD")
        score = round(0.45 * ripeness + 0.40 * localization + 0.15 * min(stable_frames / 10, 1), 4)
        if any(reason in reasons for reason in ("LOCALIZATION_CONFIDENCE_LOW", "TRACK_NOT_STABLE", "STAGE_REQUIRES_HUMAN_REVIEW_OR_PROTECTION")):
            status = "REVIEW"
        elif reasons:
            status = "REJECTED"
        else:
            status = "PROPOSAL_APPROVED_NOT_EXECUTED"
            reasons.append("CONFIGURED_SOFTWARE_GATES_PASSED_NOT_PHYSICAL_SAFETY_VALIDATION")
        result = {
            "status": "ANALYZED",
            "harvest_mode": harvest_mode,
            "selected_stages": sorted(allowed_stages),
            "decisions": [{
                "target_id": target_id.strip() or "unnamed-candidate",
                "candidate_stage": candidate_stage,
                "status": status,
                "score": score,
                "reasons": reasons,
            }],
            "actuator_commands_sent": False,
            "limitations": [
                "The score is a heuristic, not a calibrated probability.",
                "The uploaded image is not processed by a trained detector.",
                "No collision validation or physical robot safety certification is provided.",
            ],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    st.session_state["analysis_result"] = result

if "analysis_result" in st.session_state:
    result = st.session_state["analysis_result"]
    st.divider()
    st.header("3. Analysis result")
    if result["status"] == "SAFE_HOLD":
        st.error("SAFE HOLD — check sensor inputs before considering a candidate.")
        st.write("Reasons:", ", ".join(result["sensor_reasons"]))
    else:
        decision = result["decisions"][0]
        status = decision["status"]
        if status == "PROPOSAL_APPROVED_NOT_EXECUTED":
            st.success("Software checks passed for this proposal — nothing was executed.")
        elif status == "REVIEW":
            st.warning("Human review required.")
        else:
            st.error("Candidate rejected by the configured example rules.")
        metric_a, metric_b, metric_c = st.columns(3)
        metric_a.metric("Decision", status.replace("_", " "))
        metric_b.metric("Example score", f'{decision["score"]:.3f}')
        metric_c.metric("Actuator commands", "None")
        st.write("**Decision reasons**")
        if decision["reasons"]:
            for reason in decision["reasons"]:
                st.write(f"- {reason}")
        else:
            st.write("No rule-based warning was triggered.")
    st.code(json.dumps(result, indent=2), language="json")
    st.download_button(
        "Download JSON audit example",
        data=json.dumps(result, indent=2),
        file_name="coconut_harvest_ai_demo_result.json",
        mime="application/json",
        use_container_width=True,
    )

st.divider()
st.header("4. End-to-end robot task simulation")
st.caption(
    "This separate panel uses explicitly supplied example evidence. It does not derive 3D "
    "position from the uploaded image, simulate robot physics, or send hardware commands."
)
with st.expander("Configure a simulated target and safety gates", expanded=False):
    from apps.pui89_app.robot_workflow import Candidate, run_simulated_workflow

    sim_left, sim_right = st.columns(2)
    with sim_left:
        sim_target_id = st.text_input("Simulation target ID", value="coconut-sim-01")
        sim_confidence = st.slider("Supplied detection confidence", 0.0, 1.0, 0.90, 0.01)
        sim_x = st.number_input("Camera/world X (m; supplied)", value=1.0, min_value=-10.0, max_value=10.0, step=0.1)
        sim_y = st.number_input("Camera/world Y (m; supplied)", value=0.5, min_value=-10.0, max_value=10.0, step=0.1)
        sim_z = st.number_input("Camera/world Z (m; supplied)", value=1.2, min_value=-10.0, max_value=15.0, step=0.1)
    with sim_right:
        sim_uncertainty = st.number_input("Localization uncertainty (m; supplied)", value=0.04, min_value=0.0, max_value=5.0, step=0.01)
        sim_track_age = st.slider("Track age (frames; supplied)", 0, 30, 8)
        sim_age_s = st.slider("Observation age (seconds)", 0.0, 2.0, 0.1, 0.05)
        sim_clearance = st.number_input("Obstacle clearance (m; supplied)", value=0.5, min_value=0.0, max_value=5.0, step=0.05)
        sim_reachable = st.checkbox("Reachability independently confirmed (input only)", value=False)
    sim_human_approval = st.checkbox("Approve this simulated task sequence", value=False)
    sim_emergency_stop = st.checkbox("Emergency stop active", value=False)
    if st.button("Run simulation-only workflow", use_container_width=True):
        now_s = 10.0
        sim_candidate = Candidate(
            target_id=sim_target_id.strip() or "unnamed-target",
            confidence=sim_confidence,
            bbox_xyxy_pixels=(10.0, 10.0, 50.0, 50.0),
            world_position_m=(float(sim_x), float(sim_y), float(sim_z)),
            localization_uncertainty_m=float(sim_uncertainty),
            track_age_frames=int(sim_track_age),
            timestamp_s=now_s - float(sim_age_s),
            obstacle_clearance_m=float(sim_clearance),
            reachable=sim_reachable,
        )
        sim_report = run_simulated_workflow(
            [sim_candidate],
            now_s=now_s,
            human_approved=sim_human_approval,
            emergency_stop=sim_emergency_stop,
        ).to_dict()
        st.session_state["robot_workflow_report"] = sim_report

if "robot_workflow_report" in st.session_state:
    sim_report = st.session_state["robot_workflow_report"]
    if sim_report["status"] == "COMPLETED_SIMULATION":
        st.success("Simulated task sequence completed. No physical robot action occurred.")
    elif sim_report["status"] == "AWAITING_HUMAN_APPROVAL":
        st.warning("Awaiting approval. No simulated action sequence was emitted.")
    else:
        st.error(f"Workflow stopped: {sim_report['status']}")
    st.code(json.dumps(sim_report, indent=2), language="json")
    st.download_button(
        "Download simulated workflow report",
        data=json.dumps(sim_report, indent=2),
        file_name="coconut_harvest_ai_robot_workflow.json",
        mime="application/json",
        use_container_width=True,
    )

st.divider()
st.caption(
    "Research prototype only. Never connect this demo directly to motors, cutters, or manipulators. "
    "Real-world use requires a validated detector, calibrated sensors, independent safety checks, "
    "and supervised testing."
)


# Local-first operator inspection records. This workflow is separate from the
# illustrative candidate demo above and stores data only in the local workspace.
st.divider()
st.header("5. Operator inspection records")
st.caption(
    "Create or reopen a local inspection, preserve imported image evidence, "
    "record human maturity assessments and export a traceable JSON report. "
    "This section does not run a maturity detector or control a robot."
)

from apps.pui89_app.inspection_records import InspectionError, InspectionRecordStore

default_workspace = Path.home() / ".pui89" / "coconut-inspections"
workspace_path = os.environ.get("PUI89_COCONUT_WORKSPACE", str(default_workspace)).strip()
try:
    inspection_store = InspectionRecordStore(workspace_path)
    st.caption(f"Local workspace: {inspection_store.workspace}")
    inspection_index = inspection_store.list_inspections()

    with st.expander("Create a new inspection", expanded=not bool(inspection_index)):
        new_operator = st.text_input("Operator alias", value="operator-01", key="record_new_operator")
        new_site = st.text_input("Farm/site code (optional)", key="record_new_site")
        new_notes = st.text_area("Inspection notes (optional)", key="record_new_notes")
        if st.button("Create inspection record", key="record_create_button"):
            try:
                created = inspection_store.create_inspection(
                    operator_alias=new_operator,
                    site_code=new_site,
                    notes=new_notes,
                )
                st.session_state["pui89_inspection_selector"] = created["inspection_id"]
                st.success(f"Created inspection {created['inspection_id']}")
                st.rerun()
            except InspectionError as exc:
                st.error(f"Inspection could not be created: {exc}")

    inspection_index = inspection_store.list_inspections()
    if inspection_index:
        inspection_ids = [item["inspection_id"] for item in inspection_index]
        current_selection = st.session_state.get("pui89_inspection_selector")
        selected_index = inspection_ids.index(current_selection) if current_selection in inspection_ids else 0
        selected_inspection_id = st.selectbox(
            "Open inspection",
            options=inspection_ids,
            index=selected_index,
            key="pui89_inspection_selector",
        )
        active_record = inspection_store.get_inspection(selected_inspection_id)

        st.write(
            f"**Status:** {active_record['status']}  ·  "
            f"**Images:** {len(active_record['images'])}  ·  "
            f"**Candidates:** {len(active_record['candidates'])}"
        )
        st.caption(
            f"Operator: {active_record['metadata']['operator_alias']}  ·  "
            f"Site: {active_record['metadata']['site_code'] or 'not supplied'}"
        )

        with st.expander("Import an image into this inspection", expanded=not bool(active_record["images"])):
            record_upload = st.file_uploader(
                "Select a JPG, PNG or WebP orchard image",
                type=["jpg", "jpeg", "png", "webp"],
                key=f"record_upload_{selected_inspection_id}",
            )
            source_reference = st.text_input(
                "Source reference (optional)", key=f"record_source_{selected_inspection_id}"
            )
            rights_status = st.selectbox(
                "Image reuse-rights status",
                options=["unverified", "pending_review", "cleared", "restricted", "unknown"],
                index=0,
                key=f"record_rights_{selected_inspection_id}",
                help="This is a recorded status only; it does not independently verify legal rights.",
            )
            if st.button("Preserve image in local inspection", key=f"record_import_{selected_inspection_id}"):
                if record_upload is None:
                    st.error("Select an image first.")
                else:
                    try:
                        imported = inspection_store.import_image(
                            selected_inspection_id,
                            record_upload.getvalue(),
                            filename=record_upload.name,
                            source_type="user_provided",
                            source_reference=source_reference,
                            rights_status=rights_status,
                        )
                        st.success(
                            f"Image stored with SHA-256 {imported['sha256']} "
                            f"({imported['width']} × {imported['height']})"
                        )
                        st.rerun()
                    except InspectionError as exc:
                        st.error(f"Image was not imported: {exc}")

        active_record = inspection_store.get_inspection(selected_inspection_id)
        if active_record["images"]:
            st.subheader("Evidence images")
            image_labels = {
                item["sha256"]: f"{item['original_filename']} · {item['sha256'][:12]}"
                for item in active_record["images"]
            }
            selected_image_hash = st.selectbox(
                "Image for assessment",
                options=list(image_labels),
                format_func=lambda value: image_labels[value],
                key=f"record_image_{selected_inspection_id}",
            )
            selected_image = next(
                item for item in active_record["images"] if item["sha256"] == selected_image_hash
            )
            image_bytes = inspection_store.read_image(selected_inspection_id, selected_image_hash)
            st.image(
                image_bytes,
                caption=f"Preserved source image · SHA-256 {selected_image_hash}",
                use_container_width=True,
            )

            with st.form(f"record_annotation_form_{selected_inspection_id}"):
                st.subheader("Record a human assessment")
                candidate_id = st.text_input("Candidate ID", value="fruit-01")
                maturity_label = st.selectbox(
                    "Maturity assessment",
                    options=[
                        "young_green", "mature_green", "yellow",
                        "brown_aging", "unknown", "review",
                    ],
                    format_func=lambda value: {
                        "young_green": "Young green",
                        "mature_green": "Mature green",
                        "yellow": "Yellow",
                        "brown_aging": "Brown / aging",
                        "unknown": "Unknown",
                        "review": "Needs review",
                    }[value],
                )
                reviewer_alias = st.text_input(
                    "Reviewer alias",
                    value=active_record["metadata"]["operator_alias"],
                )
                assessment_reason = st.text_area("Reason / uncertainty notes (optional)")
                include_bbox = st.checkbox("Add normalized bounding-box coordinates")
                bbox_values = None
                if include_bbox:
                    col_x, col_y, col_w, col_h = st.columns(4)
                    with col_x:
                        bbox_x = st.number_input("X", min_value=0.0, max_value=1.0, value=0.1, step=0.01)
                    with col_y:
                        bbox_y = st.number_input("Y", min_value=0.0, max_value=1.0, value=0.1, step=0.01)
                    with col_w:
                        bbox_w = st.number_input("Width", min_value=0.0, max_value=1.0, value=0.3, step=0.01)
                    with col_h:
                        bbox_h = st.number_input("Height", min_value=0.0, max_value=1.0, value=0.3, step=0.01)
                    bbox_values = [bbox_x, bbox_y, bbox_w, bbox_h]
                save_assessment = st.form_submit_button("Save assessment revision")
            if save_assessment:
                try:
                    revision = inspection_store.add_annotation(
                        selected_inspection_id,
                        candidate_id=candidate_id,
                        image_sha256=selected_image_hash,
                        maturity_label=maturity_label,
                        reviewer_alias=reviewer_alias,
                        reason=assessment_reason,
                        bbox_xywh_normalized=bbox_values,
                    )
                    st.success(
                        f"Saved revision {revision['revision']} for {candidate_id}. "
                        "Earlier revisions are preserved."
                    )
                    st.rerun()
                except InspectionError as exc:
                    st.error(f"Assessment was not saved: {exc}")

        active_record = inspection_store.get_inspection(selected_inspection_id)
        st.subheader("Assessment history")
        if active_record["candidates"]:
            for candidate in active_record["candidates"]:
                latest = candidate["revisions"][-1]
                with st.expander(
                    f"{candidate['candidate_id']} · {latest['maturity_label']} · "
                    f"{len(candidate['revisions'])} revision(s)"
                ):
                    st.json(candidate)
        else:
            st.info("No candidate assessments have been recorded yet.")

        report = inspection_store.export_report(selected_inspection_id)
        report_json = json.dumps(report, ensure_ascii=False, indent=2)
        report_col, save_col = st.columns(2)
        with report_col:
            st.download_button(
                "Download inspection JSON report",
                data=report_json,
                file_name=f"{selected_inspection_id}-inspection-report.json",
                mime="application/json",
                key=f"record_download_{selected_inspection_id}",
                use_container_width=True,
            )
        with save_col:
            if st.button("Save report to local workspace", key=f"record_save_{selected_inspection_id}", use_container_width=True):
                try:
                    report_path = inspection_store.write_report(selected_inspection_id)
                    st.success(f"Saved locally: {report_path}")
                except OSError as exc:
                    st.error(f"Report could not be saved: {type(exc).__name__}")
    else:
        st.info("Create an inspection record to begin.")
except (InspectionError, OSError) as exc:
    st.error(f"Local inspection workspace is unavailable: {type(exc).__name__}: {exc}")

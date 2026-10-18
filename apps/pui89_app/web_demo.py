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
    target_id = st.text_input("Candidate ID", value="coconut-01", max_chars=80)
    ripeness = st.slider("Ripeness evidence score", 0.0, 1.0, 0.91, 0.01)
    localization = st.slider("Localization confidence", 0.0, 1.0, 0.94, 0.01)
    distance = st.slider("Estimated distance (m)", 0.0, 8.0, 2.1, 0.1)
    clearance = st.slider("Estimated obstacle clearance (m)", 0.0, 1.5, 0.45, 0.05)
    stable_frames = st.slider("Consecutive stable tracking frames", 0, 30, 12)


with st.expander("Optional: run a trusted local coconut detector", expanded=False):
    st.caption(
        "This optional feature runs a user-supplied model file on the local CPU. "
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
        detector_confidence = st.slider(
            "Detection confidence threshold", 0.05, 0.95, 0.25, 0.05,
            key="local_detector_confidence",
        )
        if st.button("Run local image detection", use_container_width=True):
            try:
                from PIL import Image, ImageDraw

                with st.spinner("Running local inference on CPU..."):
                    model, coconut_ids = _load_cached_local_model(local_model_path)
                    image = Image.open(io.BytesIO(upload.getvalue())).convert("RGB")
                    detections = detect_coconuts(
                        model, image, coconut_ids, confidence=detector_confidence
                    )
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
                    "inference_device": "cpu",
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
            "sensor_reasons": sensor_reasons,
            "decisions": [],
            "actuator_commands_sent": False,
        }
    else:
        reasons = []
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
        if any(reason in reasons for reason in ("LOCALIZATION_CONFIDENCE_LOW", "TRACK_NOT_STABLE")):
            status = "REVIEW"
        elif reasons:
            status = "REJECTED"
        else:
            status = "PROPOSAL_APPROVED_NOT_EXECUTED"
            reasons.append("CONFIGURED_SOFTWARE_GATES_PASSED_NOT_PHYSICAL_SAFETY_VALIDATION")
        result = {
            "status": "ANALYZED",
            "decisions": [{
                "target_id": target_id.strip() or "unnamed-candidate",
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

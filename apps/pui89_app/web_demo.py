"""Interactive Streamlit demo for Coconut Harvest AI decision support.

This is a transparent rule-based demonstration, not a trained image detector.
Uploaded images are displayed for context; they are not automatically analysed.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone

import streamlit as st

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
st.caption(
    "Research prototype only. Never connect this demo directly to motors, cutters, or manipulators. "
    "Real-world use requires a validated detector, calibrated sensors, independent safety checks, "
    "and supervised testing."
)

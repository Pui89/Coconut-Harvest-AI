"""PUI89 Coconut Intelligence — local-first inspection workspace."""
from __future__ import annotations
import io, json, os
from pathlib import Path
import streamlit as st
from PIL import Image
from apps.pui89_app.inspection_workspace import (
    LABELS, MAX_IMAGE_BYTES, add_annotation, create_inspection,
    export_report, image_path_for, list_inspections, load_inspection
)
DEFAULT_WORKSPACE = Path.home() / ".pui89" / "coconut-inspections"
WORKSPACE = Path(os.environ.get("PUI89_COCONUT_WORKSPACE", str(DEFAULT_WORKSPACE))).expanduser()
LABEL_NAMES = {
    "young": "Young green / อ่อน", "developing_green": "Developing green / กำลังพัฒนา",
    "mature_green": "Mature green / แก่เขียว", "brown_aging": "Brown / aging / น้ำตาล-แก่จัด",
    "unknown_needs_review": "Unknown — needs review / ไม่แน่ใจ"
}
st.set_page_config(page_title="PUI89 Coconut Intelligence", page_icon="🥥", layout="wide")
st.title("🥥 PUI89 Coconut Intelligence")
st.caption("Local-first coconut inspection workspace · Human-reviewed evidence · No robot control")
st.info("This product records and organises human inspections. It does not automatically classify photos, certify maturity, recommend cutting, or control a harvesting robot.")
create_tab, review_tab, export_tab = st.tabs(["New inspection / สร้างรายการ", "Review & annotate / ตรวจสอบ", "Reports / รายงาน"])

with create_tab:
    st.subheader("Create an inspection")
    with st.form("create_inspection_form", clear_on_submit=True):
        uploaded = st.file_uploader("Coconut image / ภาพมะพร้าว", type=["jpg","jpeg","png","webp"])
        source = st.text_input("Image source and permission basis / ที่มาของภาพและสิทธิ์ใช้งาน", placeholder="e.g. Original photo taken by operator")
        rights = st.checkbox("I confirm I am authorised to use and store this image / ยืนยันว่ามีสิทธิ์ใช้ภาพนี้")
        c1,c2 = st.columns(2)
        with c1:
            site = st.text_input("Farm / site code (optional)")
            operator = st.text_input("Operator alias (optional)")
        with c2:
            notes = st.text_area("Inspection notes / บันทึกเพิ่มเติม", max_chars=2000)
        submitted = st.form_submit_button("Create inspection / สร้างรายการ", type="primary", use_container_width=True)
    if submitted:
        if uploaded is None:
            st.error("Please select an image.")
        elif uploaded.size > MAX_IMAGE_BYTES:
            st.error("Image exceeds the 10 MB limit.")
        else:
            try:
                raw=uploaded.getvalue()
                with Image.open(io.BytesIO(raw)) as im: im.verify()
                with Image.open(io.BytesIO(raw)) as im: fmt, width, height = im.format or "", im.width, im.height
                record=create_inspection(WORKSPACE, image_bytes=raw, image_extension=Path(uploaded.name).suffix,
                    image_format=fmt, image_width=width, image_height=height, original_filename=uploaded.name,
                    source_description=source, rights_confirmed=rights, site_code=site,
                    operator_alias=operator, notes=notes)
                st.success("Inspection created: " + record["inspection_id"])
                st.caption("Image SHA-256: " + record["image"]["sha256"])
            except Exception as exc:
                st.error("Could not create inspection: " + str(exc))

with review_tab:
    records=list_inspections(WORKSPACE)
    if not records:
        st.info("No local inspections yet. Create the first inspection in the previous tab.")
    else:
        choices={f"{r['created_at'][:19]} · {r['site_code'] or 'No site'} · {r['inspection_id'][:8]}":r["inspection_id"] for r in records}
        selected=st.selectbox("Select inspection", list(choices))
        selected_id=choices[selected]
        record=load_inspection(WORKSPACE, selected_id)
        st.write(f"**Revision:** {record['revision']} · **Image:** {record['image']['width']} × {record['image']['height']}")
        st.image(str(image_path_for(WORKSPACE, selected_id)), caption="Original image — stored unchanged")
        st.caption("SHA-256: " + record["image"]["sha256"])
        st.write("**Source:** " + record["image"]["source_description"])
        st.write("**Existing annotations**")
        if record["annotations"]:
            st.dataframe([{"Candidate":a["candidate_id"],"Label":LABEL_NAMES[a["label"]],
                "Reviewer":a["reviewer_alias"],"Status":a["status"],"Box (normalised)":a["bbox_normalized_xyxy"]}
                for a in record["annotations"]], use_container_width=True, hide_index=True)
        else: st.caption("No fruit candidates annotated yet.")
        st.divider()
        st.subheader("Add a human-reviewed fruit annotation")
        st.caption("Enter normalised box coordinates from 0 to 1: top-left (x1,y1), bottom-right (x2,y2).")
        with st.form("add_annotation_form", clear_on_submit=True):
            candidate=st.text_input("Candidate ID", value=f"fruit-{len(record['annotations'])+1:02d}")
            label=st.selectbox("Visual appearance label", LABELS, format_func=lambda x:LABEL_NAMES[x])
            reviewer=st.text_input("Reviewer alias")
            c1,c2=st.columns(2)
            with c1:
                x1=st.number_input("Left x1",0.0,1.0,0.1,0.01); y1=st.number_input("Top y1",0.0,1.0,0.1,0.01)
            with c2:
                x2=st.number_input("Right x2",0.0,1.0,0.8,0.01); y2=st.number_input("Bottom y2",0.0,1.0,0.8,0.01)
            reason=st.text_input("Reason for uncertainty / notes (optional)")
            add=st.form_submit_button("Save annotation as new revision", use_container_width=True)
        if add:
            try:
                updated=add_annotation(WORKSPACE, selected_id, candidate_id=candidate, label=label,
                    reviewer_alias=reviewer, x1=x1,y1=y1,x2=x2,y2=y2,reason=reason)
                st.success(f"Saved revision {updated['revision']}. Previous events remain in the audit history.")
                st.rerun()
            except Exception as exc: st.error("Annotation not saved: " + str(exc))

with export_tab:
    records=list_inspections(WORKSPACE)
    if not records: st.info("Create an inspection before exporting a report.")
    else:
        choices={f"{r['created_at'][:19]} · {r['inspection_id'][:8]}":r["inspection_id"] for r in records}
        selected=st.selectbox("Inspection to export",list(choices),key="export_inspection")
        report=export_report(WORKSPACE,choices[selected])
        st.json(report)
        st.download_button("Download inspection report (JSON)",data=json.dumps(report,ensure_ascii=False,indent=2),
            file_name=f"pui89-coconut-inspection-{choices[selected][:8]}.json",
            mime="application/json",use_container_width=True)
st.divider()
st.caption(f"Local workspace: {WORKSPACE} · Images remain on this device unless you explicitly export or share them.")

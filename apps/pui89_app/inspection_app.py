"""PUI89 Coconut Intelligence — local-first, human-reviewed inspection app."""
from __future__ import annotations
import io, json, os, uuid
from pathlib import Path
import streamlit as st
from PIL import Image, ImageDraw, ImageStat, ImageFilter
from apps.pui89_app.inspection_workspace import (
    LABELS, MAX_IMAGE_BYTES, add_annotation, create_inspection, export_report,
    export_annotation_manifest, image_path_for, list_inspections, load_inspection,
    record_quality_review
)

DEFAULT_WORKSPACE = Path.home() / ".pui89" / "coconut-inspections"
WORKSPACE = Path(os.environ.get("PUI89_COCONUT_WORKSPACE", str(DEFAULT_WORKSPACE))).expanduser()
LABEL_NAMES = {
    "young_green": "Young green / อ่อน",
    "mature_green": "Mature green / แก่เขียว",
    "yellow": "Yellow / เหลือง",
    "brown_aging": "Brown / aging / น้ำตาล-แก่จัด",
    "unknown_needs_review": "Unknown — needs review / ไม่แน่ใจ",
    "young": "Legacy label: young (review taxonomy)",
    "developing_green": "Legacy label: developing green (review taxonomy)",
}

def inspect_image_quality(image):
    """Deterministic image-screening indicators; not a validated quality score."""
    gray = image.convert("L")
    sample = gray.copy()
    sample.thumbnail((256, 256))
    stats = ImageStat.Stat(sample)
    brightness = round(stats.mean[0], 2)
    contrast = round(stats.stddev[0], 2)
    hist = sample.histogram()
    total = max(1, sum(hist))
    clipped = round((sum(hist[:5]) + sum(hist[-5:])) / total, 4)
    edges = sample.filter(ImageFilter.FIND_EDGES)
    edge_proxy = round(ImageStat.Stat(edges).mean[0], 2)
    flags = []
    if image.width < 640 or image.height < 480: flags.append("LOW_RESOLUTION")
    if brightness < 35: flags.append("POSSIBLY_TOO_DARK")
    if brightness > 220: flags.append("POSSIBLY_OVEREXPOSED")
    if contrast < 20: flags.append("LOW_CONTRAST")
    if clipped > 0.15: flags.append("HIGHLIGHT_OR_SHADOW_CLIPPING")
    return {"assessment_method": "PIL_grayscale_heuristics_v1",
            "brightness_mean_0_255": brightness, "contrast_stddev_0_255": contrast,
            "clipped_pixel_fraction_approx": clipped, "edge_strength_proxy": edge_proxy,
            "flags": flags, "machine_quality_score": None,
            "interpretation": "SCREENING_ONLY_REQUIRES_HUMAN_REVIEW"}

def bilingual_report_markdown(report):
    record = report["record"]
    q = record.get("image_quality", {})
    lines = [
        "# PUI89 Coconut Intelligence — Inspection Report / รายงานการตรวจสอบ",
        "", "## Record / ข้อมูลรายการ",
        f"- Inspection ID: {record['inspection_id']}",
        f"- Batch ID: {record.get('batch_id') or '—'}",
        f"- Site / แปลง: {record.get('site_code') or '—'}",
        f"- Operator / ผู้ตรวจ: {record.get('operator_alias') or '—'}",
        f"- Captured image / ภาพ: {record['image']['original_filename']}",
        f"- Dimensions / ขนาด: {record['image']['width']} × {record['image']['height']}",
        f"- SHA-256: {record['image']['sha256']}",
        f"- Source / ที่มาภาพ: {record['image']['source_description']}",
        "", "## Image quality screening / การคัดกรองคุณภาพภาพ",
        f"- Brightness / ความสว่างเฉลี่ย: {q.get('brightness_mean_0_255', 'not assessed')}",
        f"- Contrast / คอนทราสต์: {q.get('contrast_stddev_0_255', 'not assessed')}",
        f"- Flags / ข้อสังเกต: {', '.join(q.get('flags', [])) or 'None flagged / ไม่พบธงเตือน'}",
        "- This is a heuristic screen, not a validated quality score. / เป็นเพียงการคัดกรองด้วยฮิวริสติก ไม่ใช่คะแนนคุณภาพที่ผ่านการตรวจสอบ",
        "", "## Human annotations / การระบุผลโดยมนุษย์",
    ]
    if record["annotations"]:
        for a in record["annotations"]:
            lines.append(f"- {a['candidate_id']}: {LABEL_NAMES[a['label']]} | {a['status']} | box={a['bbox_normalized_xyxy']} | reviewer={a['reviewer_alias']}")
    else:
        lines.append("- No annotations / ยังไม่มีการระบุผล")
    lines += ["", "## Decision boundaries / ขอบเขตการตัดสินใจ",
        "- No automatic classification was performed. / ไม่มีการจำแนกภาพโดยอัตโนมัติ",
        "- Human review is required. / ต้องให้มนุษย์ตรวจสอบ",
        "- This report does not authorise harvesting or robot movement. / รายงานนี้ไม่อนุญาตให้เก็บเกี่ยวหรือสั่งการหุ่นยนต์",
        "- Accuracy and field performance are not established. / ยังไม่มีการยืนยันความแม่นยำหรือสมรรถนะภาคสนาม"]
    return "\n".join(lines) + "\n"

st.set_page_config(page_title="PUI89 Coconut Intelligence", page_icon="🥥", layout="wide")
st.title("🥥 PUI89 Coconut Intelligence")
st.caption("Local-first inspection · Human-reviewed evidence · EN / TH · No robot control")
st.warning("This is an internal alpha. Quality indicators are heuristics; maturity labels are human-entered. No automated maturity decision, harvest authorisation, or robot control is provided.")
create_tab, review_tab, report_tab, dataset_tab = st.tabs([
    "New batch / สร้างชุดภาพ", "Review & annotate / ตรวจสอบ", "Reports / รายงาน", "Dataset manifest / ชุดข้อมูล"
])

with create_tab:
    st.subheader("Create a multi-image inspection batch / สร้างชุดการตรวจหลายภาพ")
    with st.form("create_inspection_form", clear_on_submit=True):
        uploads = st.file_uploader("Select up to 10 coconut photos / เลือกภาพมะพร้าวไม่เกิน 10 ภาพ",
            type=["jpg", "jpeg", "png", "webp"], accept_multiple_files=True)
        source = st.text_input("Image source and permission basis / ที่มาของภาพและสิทธิ์ใช้งาน",
            placeholder="Original photo taken by operator / ภาพถ่ายโดยผู้ตรวจ")
        rights = st.checkbox("I confirm I am authorised to use and store every selected image / ยืนยันสิทธิ์ใช้และจัดเก็บภาพทุกภาพ")
        c1, c2 = st.columns(2)
        with c1:
            site = st.text_input("Farm / site code (optional) / รหัสแปลง")
            operator = st.text_input("Operator alias / ผู้ตรวจ")
        with c2:
            notes = st.text_area("Inspection notes / บันทึกเพิ่มเติม", max_chars=2000)
        submitted = st.form_submit_button("Create batch / สร้างชุดรายการ", type="primary", use_container_width=True)
    if submitted:
        if not uploads: st.error("Select at least one image / กรุณาเลือกภาพ")
        elif len(uploads) > 10: st.error("Maximum 10 images per batch / ไม่เกิน 10 ภาพต่อชุด")
        elif sum(u.size for u in uploads) > 50 * 1024 * 1024: st.error("Batch exceeds 50 MB total / ขนาดรวมเกิน 50 MB")
        elif any(u.size > MAX_IMAGE_BYTES for u in uploads): st.error("Each image must be 10 MB or less / ภาพละไม่เกิน 10 MB")
        else:
            batch_id = uuid.uuid4().hex
            created, errors = [], []
            for uploaded in uploads:
                try:
                    raw = uploaded.getvalue()
                    with Image.open(io.BytesIO(raw)) as im:
                        im.verify()
                    with Image.open(io.BytesIO(raw)) as im:
                        fmt, width, height = im.format or "", im.width, im.height
                        quality = inspect_image_quality(im.copy())
                    record = create_inspection(WORKSPACE, image_bytes=raw,
                        image_extension=Path(uploaded.name).suffix, image_format=fmt,
                        image_width=width, image_height=height, original_filename=uploaded.name,
                        source_description=source, rights_confirmed=rights, site_code=site,
                        operator_alias=operator, notes=notes, image_quality=quality, batch_id=batch_id)
                    created.append(record)
                except Exception as exc:
                    errors.append(f"{uploaded.name}: {exc}")
            if created: st.success(f"Created {len(created)} inspection(s) in batch {batch_id[:8]}. / สร้างรายการสำเร็จ {len(created)} ภาพ")
            for record in created:
                st.caption(f"{record['image']['original_filename']} · SHA-256 {record['image']['sha256'][:16]}…")
            for error in errors: st.error(error)
            if errors and created: st.warning("Some images failed; successful records were retained separately. / บางภาพไม่สำเร็จ แต่รายการที่สำเร็จยังถูกเก็บไว้")

with review_tab:
    records = list_inspections(WORKSPACE)
    if not records:
        st.info("No local inspections yet. / ยังไม่มีรายการ")
    else:
        choices = {f"{r['created_at'][:19]} · {r['site_code'] or 'No site'} · {r['image']['original_filename']} · {r['inspection_id'][:8]}": r["inspection_id"] for r in records}
        selected = st.selectbox("Select image / เลือกภาพ", list(choices))
        selected_id = choices[selected]
        record = load_inspection(WORKSPACE, selected_id)
        st.write(f"**Revision:** {record['revision']} · **Image:** {record['image']['width']} × {record['image']['height']} · **Batch:** {(record.get('batch_id') or '—')[:8]}")
        image_path = image_path_for(WORKSPACE, selected_id)
        with Image.open(image_path) as source_image:
            preview = source_image.convert("RGB").copy()
        st.image(preview, caption="Original image — unchanged / ภาพต้นฉบับไม่ถูกแก้ไข", use_container_width=True)
        st.caption("SHA-256: " + record["image"]["sha256"] + " · " + record["image"]["source_description"])
        q = record.get("image_quality", {})
        st.subheader("Image quality / คุณภาพภาพ")
        st.json(q)
        st.caption("Brightness, contrast, clipping and edge indicators are screening heuristics only; they do not determine whether an image is suitable for training.")
        with st.form("quality_review_form"):
            st.write("Human visibility review / ให้ผู้ตรวจประเมิน")
            qr = st.text_input("Reviewer alias / ผู้ตรวจ", key="quality_reviewer")
            visibility = st.selectbox("Visibility / การมองเห็น", ["clear", "partial", "poor", "unknown"])
            occlusion = st.selectbox("Occlusion / การบดบัง", ["none", "minor", "major", "unknown"])
            qnotes = st.text_input("Notes / หมายเหตุ", max_chars=1000)
            qsave = st.form_submit_button("Save quality review / บันทึกการประเมิน")
        if qsave:
            try:
                updated = record_quality_review(WORKSPACE, selected_id, reviewer_alias=qr,
                    visibility=visibility, occlusion=occlusion, notes=qnotes)
                st.success(f"Quality review saved as revision {updated['revision']}.")
                st.rerun()
            except Exception as exc: st.error("Quality review not saved: " + str(exc))
        st.divider()
        st.subheader("Fruit annotations / ระบุตำแหน่งผลมะพร้าว")
        st.caption("Adjust the four normalised coordinates; the preview updates before saving. This is a coordinate-based preview, not drag-and-drop drawing. / ปรับพิกัด 0–1 และดูกรอบตัวอย่างก่อนบันทึก")
        c1, c2 = st.columns(2)
        with c1:
            x1 = st.slider("Left x1", 0.0, 0.99, 0.10, 0.01, key="box_x1")
            y1 = st.slider("Top y1", 0.0, 0.99, 0.10, 0.01, key="box_y1")
        with c2:
            x2 = st.slider("Right x2", 0.01, 1.0, 0.80, 0.01, key="box_x2")
            y2 = st.slider("Bottom y2", 0.01, 1.0, 0.80, 0.01, key="box_y2")
        if x1 < x2 and y1 < y2:
            overlay = preview.copy()
            draw = ImageDraw.Draw(overlay)
            draw.rectangle((int(x1*overlay.width), int(y1*overlay.height),
                            int(x2*overlay.width), int(y2*overlay.height)), outline=(0, 220, 255), width=max(2, overlay.width//400))
            st.image(overlay, caption="Bounding-box preview / ตัวอย่างกรอบตำแหน่ง", use_container_width=True)
        else:
            st.error("Coordinates must form a box / พิกัดต้องสร้างกรอบสี่เหลี่ยม")
        with st.form("add_annotation_form", clear_on_submit=True):
            candidate = st.text_input("Candidate ID", value=f"fruit-{len(record['annotations'])+1:02d}")
            label = st.selectbox("Visual appearance / ลักษณะภายนอก", LABELS, format_func=lambda x: LABEL_NAMES[x])
            reviewer = st.text_input("Annotation reviewer / ผู้ระบุผล")
            reason = st.text_input("Uncertainty / reason / เหตุผลหรือความไม่แน่นอน", max_chars=1000)
            add = st.form_submit_button("Save annotation / บันทึก", use_container_width=True)
        if add:
            try:
                updated = add_annotation(WORKSPACE, selected_id, candidate_id=candidate, label=label,
                    reviewer_alias=reviewer, x1=x1, y1=y1, x2=x2, y2=y2, reason=reason)
                st.success(f"Saved revision {updated['revision']}.")
                st.rerun()
            except Exception as exc: st.error("Annotation not saved: " + str(exc))
        st.write("**Existing annotations / รายการที่บันทึกแล้ว**")
        if record["annotations"]:
            st.dataframe([{"Candidate": a["candidate_id"], "Label": LABEL_NAMES[a["label"]],
                "Reviewer": a["reviewer_alias"], "Status": a["status"],
                "Box": a["bbox_normalized_xyxy"]} for a in record["annotations"]],
                use_container_width=True, hide_index=True)
        else: st.caption("No fruit candidates annotated yet / ยังไม่มีการระบุตำแหน่งผล")

with report_tab:
    records = list_inspections(WORKSPACE)
    if not records:
        st.info("Create an inspection first. / กรุณาสร้างรายการก่อน")
    else:
        choices = {f"{r['created_at'][:19]} · {r['image']['original_filename']} · {r['inspection_id'][:8]}": r["inspection_id"] for r in records}
        selected = st.selectbox("Inspection report / เลือกรายงาน", list(choices), key="report_inspection")
        report = export_report(WORKSPACE, choices[selected])
        st.json(report)
        report_json = json.dumps(report, ensure_ascii=False, indent=2)
        report_md = bilingual_report_markdown(report)
        st.download_button("Download JSON / ดาวน์โหลด JSON", data=report_json,
            file_name=f"pui89-coconut-inspection-{choices[selected][:8]}.json",
            mime="application/json", use_container_width=True)
        st.download_button("Download bilingual report / ดาวน์โหลดรายงาน EN-TH",
            data=report_md, file_name=f"pui89-coconut-report-{choices[selected][:8]}.md",
            mime="text/markdown", use_container_width=True)

with dataset_tab:
    st.subheader("Annotation manifest / บัญชีข้อมูลกำกับ")
    st.write("Exports verified annotation metadata and image hashes. It does not package images, approve training, or create random splits.")
    try:
        manifest = export_annotation_manifest(WORKSPACE)
        st.metric("Human annotations / จำนวน annotation", manifest["annotation_count"])
        st.download_button("Download annotation manifest JSON / ดาวน์โหลด manifest",
            data=json.dumps(manifest, ensure_ascii=False, indent=2),
            file_name="pui89-coconut-annotation-manifest.json",
            mime="application/json", use_container_width=True)
        st.json({"training_use": manifest["training_use"], "split_policy": manifest["split_policy"],
                 "limitations": manifest["limitations"]})
    except Exception as exc: st.error("Manifest export blocked: " + str(exc))

st.divider()
st.caption(f"Local workspace: {WORKSPACE} · Images remain on this device unless you explicitly export or share them. / ภาพอยู่ในอุปกรณ์นี้ เว้นแต่ผู้ใช้ส่งออกหรือแบ่งปันเอง")

# Coconut Harvest AI — 360° Intelligence Profile v1.0

**Status:** Proposed product-specific requirements; no 360° sensor integration or field validation is established.

## Mission
Build a multi-view understanding of a coconut palm and its visible bunches. Coverage should support orchard context, individual bunch inspection and per-fruit maturity review. It is not a requirement to install a panoramic camera immediately.

## Candidate workflow
1. Capture authorised RGB views around a tree/bunch from documented viewpoints.
2. Record image source, timestamp, camera pose/viewpoint where known, lighting and image quality.
3. Identify visible bunches and individual coconuts; retain bunch ID and per-fruit identity where tracking is demonstrably reliable.
4. Associate views only when evidence supports that they show the same tree/bunch/fruit. Otherwise keep them as separate observations.
5. Assess four visible classes: young green, mature green, yellow and brown; retain UNKNOWN/REVIEW for occluded, overlapping, blurred or ambiguous fruit.
6. Add calibrated depth/RGB-D or 3D reconstruction only after camera calibration, geometry and error are measured.

## Candidate AI
Object Detection, Instance Segmentation, multi-view association/tracking, image-quality assessment and human-reviewed maturity classification. VLM may assist evidence-linked review only after provenance and model gates. SLAM is not required for the current software-first milestone unless a defined mobile orchard platform needs localisation.

## 360° requirements
- Define tree-centred azimuth sectors and practical elevation bands.
- Record which fruit surfaces are visible, hidden or duplicated across views.
- Prevent double-counting when the same fruit appears in multiple views.
- Treat panorama seams, parallax, motion blur, wind-driven movement and colour/exposure differences as uncertainty sources.
- Do not infer hidden fruit, true biological maturity, harvest suitability, distance or reach from colour/panorama alone.

## Safety and exclusions
AI may prepare traceable recommendations only. Human review remains required for uncertain cases. No AI output authorises cutting, tree climbing or robot actuation. The 0–30 m perception/reach ambition remains unvalidated and is not established by 360° coverage.

## Evidence gates
Rights/provenance review → human-labelled multi-view dataset → leakage-safe tree/orchard/session split → reproducible CPU baseline → per-sector/per-class evaluation → calibrated depth/3D bench tests if justified → controlled field validation.

Report per-class precision/recall/F1, count error, duplicate/missed fruit, unknown/abstention rate, sector coverage, occlusion failure, runtime and RAM only after tests are run.

**Shared architecture:** [PUI89 360° Intelligence Architecture v1.0](https://github.com/Pui89/PUI89-Shared-AI-Core/blob/main/docs/PUI89_360_DEGREE_INTELLIGENCE_V1.0.md)

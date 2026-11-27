# PUI89 Scientific Figure & Diagram Standard

**Status:** Documentation standard / proposed workflow  
**Applies to:** Coconut Harvest AI  
**Scope:** Coconut maturity classes, fruit detection/counting, harvest decision support, perception-to-harvest workflow. Clearly label any 0–30 m operating range or harvest performance as a design target unless experimentally validated.

## 1. Purpose

Create clear, technically accurate, reproducible figures for engineering documentation, research manuscripts, technical reports, and presentations. A polished diagram is not evidence of implementation or experimental validation.

## 2. Preferred toolchain

Use free and open-source tools by default. Do not add paid subscriptions, paid APIs, metered services, cloud GPU resources, or new dependencies without explicit approval.

| Figure purpose | Preferred tools | Source / deliverable |
|---|---|---|
| AI-assisted conceptual and system diagrams | Diagram Design (after source and license review) | HTML / SVG |
| Reproducible workflows and data flows | Mermaid | `.mmd` |
| Scientific plots and experimental results | Python + Matplotlib | `.py` + SVG / PDF / PNG |
| Final vector editing and figure assembly | Inkscape | SVG |
| Geospatial and agricultural maps, where relevant | QGIS | Project + exported figure |
| Mathematical / algorithmic diagrams | LaTeX TikZ / PGFPlots | `.tex` + PDF |

Diagram Design is an optional authoring aid, not a scientific validation tool. Verify the exact repository license, dependencies, export behavior, and any external asset/font loading before adoption.

## 3. Figure integrity requirements

1. Every component, connection, unit, label, and direction must match the documented design or actual experiment.
2. Distinguish **proposed**, **simulated**, **implemented**, and **experimentally validated** elements.
3. Never present targets, estimates, simulations, or conceptual specifications as measured results.
4. Use citations for third-party methods, datasets, icons, illustrations, and adapted figures.
5. Do not fabricate metrics, test outcomes, sensor capabilities, hardware, or operating limits.
6. Keep human approval, safety gates, abstention, and safe-stop paths visible wherever relevant.
7. Use consistent terminology across figures, text, code, and data.

## 4. Reproducibility and file organization

For each publication-quality figure, retain:
- Editable source (`.mmd`, `.py`, `.tex`, or native SVG as applicable).
- Exported vector output (SVG or PDF where supported).
- Raster output (PNG) only when required by the target venue.
- Figure caption and a short description of the source data / assumptions.
- References and asset/license attribution.
- Tool and version information when relevant.

Suggested location: `docs/figures/` for figure sources and `docs/figures/exports/` for publication exports. Do not commit large generated files or binary artifacts unless they are needed and appropriate for the repository.

## 5. Publication checks

Before submission, verify the target journal's current instructions for figure dimensions, resolution, fonts, file formats, color accessibility, and AI-use disclosure. Ensure all text remains legible at final print size. Prefer vector formats for diagrams and use adequate raster resolution for photographs or raster-only plots.

## 6. Review checklist

- [ ] Scientific and engineering content checked by a human.
- [ ] Proposed / simulated / implemented / validated status stated accurately.
- [ ] All arrows, interfaces, units, and labels checked.
- [ ] Experimental plots generated from traceable data and scripts.
- [ ] Citations and third-party asset permissions checked.
- [ ] Editable source retained.
- [ ] Export inspected at the intended publication size.
- [ ] Journal-specific requirements and AI disclosure checked.

## 7. Important limitation

Using these tools does not make a paper Q1-ready or guarantee journal acceptance. Research novelty, sound methodology, appropriate experiments, statistical validity, reproducibility, and peer review remain independent requirements.

# PUI89 Free-First Engineering Resource Roadmap

**Project:** Coconut Harvest AI

Use for orchard image/data workflows and a future harvesting simulation; 0–30 m is a design challenge, not validated reach.

This is a resource and adoption plan, not a claim that every tool is installed or integrated. Start with existing Python and GitHub automation; add dependencies only when a specific test needs them.

## Priority 1 — Use now, no new dependency

| Resource | Use | Cost / safety boundary |
|---|---|---|
| [Python standard library](https://docs.python.org/3/library/) | Scenario validation, hashes, JSON/CSV reports, audit scripts | Already used by the lightweight tools; no package install needed |
| [GitHub Actions](https://docs.github.com/actions) | Repeatable CI and simulation benchmark runs | Use existing short jobs; check account usage and included minutes |
| [GitHub Issues and pull requests](https://docs.github.com/issues) | Track defects, evidence, decisions and review | Keep changes reviewable; do not store secrets in issues |
| [JSON](https://www.json.org/) and CSV reports | Machine-readable results and comparison | Include scenario/config hash, failures and limitations |
| [SHA-256](https://docs.python.org/3/library/hashlib.html) | File and configuration integrity checks | A hash proves file identity, not ownership, licence or truth |

## Priority 2 — Add only when the requirement is clear

| Resource | Potential role | Adoption gate |
|---|---|---|
| [pytest](https://docs.pytest.org/) | More expressive regression and property-style tests | Use only if already available or deliberately approved; never install silently |
| [OpenCV](https://opencv.org/) | Classical image processing and camera utilities | Check package size, platform support, and the licence for the exact distribution |
| [ONNX Runtime](https://onnxruntime.ai/) | Run compatible exported models without a hosted inference API | Require a compatible model, model-card/licence review, and measured RAM/VRAM first |
| [ROS 2](https://docs.ros.org/) | Robot messaging, lifecycle and integration tests | Defer until interfaces and simulator scenarios are stable; check OS/version support |
| [Gazebo](https://gazebosim.org/) | Physical-environment simulation | Add only for a defined simulation question; budget local disk/RAM and keep all results labelled simulated |
| [Open3D](https://www.open3d.org/) | Point clouds and 3D geometry experiments | Use only when depth/point-cloud inputs exist and the laptop can handle them |

## Project-specific next steps

- **Coconut Harvest AI:** source/licence/hash audit; tree/source/session-separated dataset splits; maturity-class baseline and per-class metrics; then camera/geometry simulation.
- **Extreme Flood Rescue AI:** scenario tests for visibility, flow assumptions, loss of GPS/comms, sensor faults, energy limits and safe stopping; 0–15 m values remain simulation parameters.
- **Multimodal Narcotics Screening AI:** test missing/conflicting modalities, calibration and time alignment, low confidence, corrupted inputs, audit trail and human review. An image or model score does not prove chemical identity.

## Rules before adding any model or dependency

1. Re-check the exact repository, model card, licence and intended-use restrictions.
2. Estimate download size, install footprint, RAM and VRAM; compare with the available machine.
3. Do not download weights or call a paid API automatically. Model preflight must remain a report-only step until explicitly reviewed.
4. Keep synthetic tests separate from labelled real-data evaluation and field validation.
5. Preserve failed cases and uncertainty. Never claim a capability because a workflow is green.
6. For high-impact screening, outputs remain triage-only and require lawful qualified human review; no automated accusation, detention, seizure or enforcement.

## Definition of done

A resource is adopted only after documenting the requirement it serves, licence/terms, machine requirements, cost exposure, test evidence and rollback path. The default is **do not add it yet** if the benefit is unclear.

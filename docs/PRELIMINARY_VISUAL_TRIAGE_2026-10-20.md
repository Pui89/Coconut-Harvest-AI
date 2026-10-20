# Preliminary visual triage of the 30-image candidate batch — 20 October 2026

## Scope and evidence

This is a quick visual screen of the image contact sheet generated from the existing GitHub Actions artifact `coconut-image-candidates` (run [39092214196](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39092214196)). The downloaded ZIP SHA-256 was verified against the GitHub artifact digest:

`da87fe2b3380fec4f5675f7c6d8b02a28f5597eaed1b03771c8ae2df4529480f`

The artifact contains 30 image files. This preliminary screen is **not** a source-rights audit, annotation review, or approval for training. Decisions below are based on thumbnail-level visual relevance only; inspect originals before final decisions.

## Preliminary decisions

| Image ID | Preliminary decision | Reason / required action |
|---|---|---|
| 0001 | Keep as review candidate | Coconut palm and visible fruit; verify source rights and inspect original. |
| 0002 | Keep for annotation correction | Visible coconut cluster; existing first-pass boxes still need overlap review and independent correction. |
| 0003 | Exclude from in-tree coconut detector dataset | Collage of harvested/cut coconut and unrelated seed-like objects; does not represent the intended in-tree detection task. Preserve provenance for audit. |
| 0004 | Keep for annotation correction | Visible green coconuts; existing boxes touching image borders need independent review. |
| 0005 | Review candidate | Palm/climber scene; inspect whether target coconuts are visible enough to label. |
| 0006 | Review candidate | Palm/climber scene with substantial occlusion; label only clearly identifiable coconuts. |
| 0007 | Exclude from in-tree coconut detector dataset | Harvesting tool close-up; no in-tree coconut targets. |
| 0008 | Review candidate for task fit | Harvesting scene; confirm visible target fruit and labelability in the original. |
| 0009 | Review candidate | Harvesting scene with palm and possible fruit; inspect original and annotation feasibility. |
| 0010 | Review candidate | Palm/climber scene with visible fruit; verify source rights and labelable boundaries. |
| 0011 | Exclude from the target-detection set unless a separate task is defined | Coconut processing/people scene; no clear in-tree fruit targets in the thumbnail. |
| 0012 | Review candidate | Palm scene; inspect target visibility and source rights. |
| 0013 | Review candidate | Climber on a palm; inspect for clearly visible target coconuts. |
| 0014 | Review candidate | Palm and fruit appear visible; inspect original and labelability. |
| 0015 | Review candidate for task fit | Person using a harvesting tool; no clearly labelable fruit targets in the thumbnail. Exclude if original confirms no targets. |
| 0016 | Review candidate for scene diversity | Plantation scene; likely useful for context but fruit targets may be too small to label. |
| 0017 | Review candidate for scene diversity | Plantation rows; check target visibility and image provenance. |
| 0018 | Exclude from image detector dataset | Map/diagram, not a photograph of coconut targets. |
| 0019 | Review candidate for scene diversity | Plantation landscape; inspect whether individual coconuts are resolvable. |
| 0020 | Review candidate for scene diversity | Plantation landscape; inspect target visibility and source rights. |
| 0021 | Review candidate for scene diversity | Palm canopy with possible fruit; inspect original resolution and labelability. |
| 0022 | Review candidate for scene diversity | Palm canopy; inspect whether individual fruit boundaries are clear. |
| 0023 | Exclude from mature-fruit detector dataset | Seedling/young plant scene, not mature coconut fruit targets. |
| 0024 | Exclude from mature-fruit detector dataset | Seedling/young plant scene, not mature coconut fruit targets. |
| 0025 | Review candidate for scene diversity | Plantation scene; inspect whether target fruits are resolvable. |
| 0026 | Review candidate only if historical/low-quality images are in scope | Archival/grayscale plantation scene; likely domain shift and low-resolution concerns. |
| 0027 | Review candidate only if historical/low-quality images are in scope | Archival/grayscale scene; assess task fit and labelability. |
| 0028 | Review candidate only if historical/low-quality images are in scope | Archival/grayscale scene; assess task fit and labelability. |
| 0029 | Exclude from coconut detector dataset | Racetrack/landscape scene, no relevant coconut targets. |
| 0030 | Review candidate only if historical/low-quality images are in scope | Grayscale plantation image; check visible targets and whether this domain belongs in the intended evaluation. |

## Required before any training

1. Confirm source-page rights, author attribution and licence terms for every retained image.
2. Inspect each retained original at full resolution; remove duplicates and images with no clearly labelable targets.
3. Apply the project's annotation policy consistently; do not guess boundaries for occluded fruit.
4. Review overlays against originals and obtain a second independent review.
5. Keep source/tree/capture groups together when creating train/validation/test splits.
6. Keep all unapproved images and draft labels outside the active training set and public repository.

## Status

**Training remains blocked.** This document records a preliminary relevance screen, not a complete dataset audit. It does not approve any image or annotation, and it makes no claim about detector accuracy.

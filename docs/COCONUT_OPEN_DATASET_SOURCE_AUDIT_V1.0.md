# PUI89 Coconut Harvest AI — Open-Source Image Dataset Source Audit v1.0

**Audit date:** 2026-11-23  
**Status:** SOURCE DISCOVERY COMPLETE — IMAGE-BY-IMAGE RIGHTS, ARCHIVE INTEGRITY AND CLASS MAPPING NOT YET VERIFIED  
**Repository:** `Pui89/Coconut-Harvest-AI`  
**Purpose:** Record candidate public image datasets before any download, annotation, training or publication.

## 1. Executive decision

Six public candidate sources were reviewed. They are not interchangeable and must not be merged by simply combining their published image counts.

- The Mendeley **Coconut tree crown** collection is the strongest first candidate for real upward-looking palm-crown scenes.
- The two Roboflow **on-tree instance-segmentation** collections are candidates for individual-fruit localisation, but their `stage1`, `stage2`, and `stage3` labels have no verified mapping to PUI89's classes.
- The Roboflow **coconut maturity classification** collection may support classification research, but its viewpoint, image composition and class adjudication are not adequately described on the public page.
- **RawRipe** offers only two coconut maturity states and its repository does not contain the original image archive.
- The second Mendeley **Coconut** collection advertises matured/immatured coconuts, but the public page does not establish the image modality or the actual file composition.

**No candidate is approved for model training by this audit.** A public page's licence label is a lead for rights review, not proof that every embedded image has independently verified provenance, permissions or suitability for PUI89.

## 2. PUI89 target classes and schema alignment

The product README describes four visible assessment classes:

1. Young Green
2. Mature Green
3. Yellow
4. Brown

These are visual appearance labels. They must not be treated as proven biological maturity, internal quality or harvest suitability without an agronomic definition and human-reviewed labels.

The existing dataset quality-gate documentation uses internal identifiers `young`, `developing_green`, `mature_green`, and `brown_aging`. These identifiers are not a self-evident one-to-one mapping to the four display names above, particularly for Yellow. **Resolve and version one canonical class dictionary before building the production manifest.** Do not silently relabel source categories.

## 3. Candidate source register

### A. Mendeley Data — Coconut tree crown

- Source: https://data.mendeley.com/datasets/w4t73tvrf8/1
- DOI: `10.17632/w4t73tvrf8.1`
- Contributor shown: Divyanth L G; institution shown: Indian Institute of Technology Kharagpur.
- Public description: 400 RGB images, 512 × 512 pixels, collected in a commercial coconut plantation during daylight using a handheld DSLR. The photographer stood near the tree trunk and photographed the crown from different elevations, angles and lighting conditions.
- Licence displayed: CC BY 4.0.
- Availability evidence: the public page displays a **Download All** control. The rendered public page does not enumerate the archive's individual files; archive retrieval, integrity and image-level inspection remain pending.
- PUI89 fit: **HIGH for crown/scene and on-tree context discovery; NOT YET SUITABLE as a four-class labelled set.** The public description does not claim four per-fruit maturity labels or instance masks.
- Action: first priority for a controlled archive inspection, if/when download is authorised and technically available. Retain attribution and DOI.

### B. Roboflow Universe — On-tree mature coconut fruit detection (college)

- Source: https://universe.roboflow.com/college-if44x/on-tree-mature-coconut-fruit-detection
- Contributor shown: `college`.
- Public listing: 268 images; one dataset version; instance-segmentation task; three labels: `stage1`, `stage2`, `stage3`.
- Licence displayed by Roboflow: Public Domain.
- Availability evidence: public image gallery and a Fork Dataset control are visible. A complete export archive and any account/export conditions have not been tested.
- PUI89 fit: **HIGH candidate for on-tree fruit localisation; maturity mapping UNVERIFIED.** The public page does not define the biological or visual meaning of the three stage labels.
- Rights caveat: treat Public Domain as the platform's displayed declaration pending source-level provenance review; record contributor/source attribution and inspect any included metadata before reuse.
- Action: retain as a separate candidate collection; do not map stage labels to PUI89 classes without source documentation and human adjudication.

### C. Roboflow Universe — On tree mature coconut fruit detection using SOLOv2 (college)

- Source: https://universe.roboflow.com/college-if44x/on-tree-mature-coconut-fruit-detection-using-solov2
- Contributor shown: `college`.
- Public listing: 495 images; two dataset versions; instance-segmentation task; three labels: `stage1`, `stage2`, `stage3`.
- Licence displayed by Roboflow: Public Domain.
- Availability evidence: public gallery and dataset/version links are visible; a complete archive export has not been tested.
- PUI89 fit: **HIGH candidate for on-tree fruit localisation; maturity mapping UNVERIFIED.**
- Duplicate risk: this collection has the same displayed contributor and similar class names as candidate B. It may overlap in source images or derive from related versions. Do not count or merge it as independent data until file hashes, perceptual duplicates, image content and version histories are compared.
- Action: retain separately pending overlap and provenance review.

### D. Roboflow Universe — Coconut_maturity_Classification (Tejaswini D)

- Source: https://universe.roboflow.com/tejaswini-d-tjrmk/coconut_maturity_classification
- Contributor shown: Tejaswini D.
- Public listing: 3,826 images; two dataset versions; classification task; six labels: `Copra`, `Mature`, `Not coconut`, `Old`, `Unlabeled`, `Young`.
- Licence displayed by Roboflow: CC BY 4.0.
- Availability evidence: public image gallery and dataset/version links are visible; a complete export archive has not been tested.
- PUI89 fit: **MEDIUM candidate for classification research; ON-TREE CONTEXT AND FOUR-CLASS COVERAGE UNVERIFIED.** The public description is blank. `Unlabeled` must not be treated as a maturity class, and `Copra`/ `Old` cannot be mapped to Brown without a defined task and review.
- Action: inspect a permitted sample and source metadata before deciding whether it belongs in the on-tree dataset or a separate off-tree classification set. Do not rely on the model accuracy displayed on the page as PUI89 evidence.

### E. RawRipe — fruit maturity recognition

- Source repository: https://github.com/ai-agriculture-circuits-and-systems/RawRipe
- Original dataset/paper: https://ieeexplore.ieee.org/document/9589215
- Repository README states 1,630 real RGB images across ten fruit types, including coconut raw (72) and ripe (78); image-level classification annotations; CC BY 4.0.
- Critical availability limitation: the repository explicitly states that the original dataset is available through IEEE Xplore and that this GitHub repository hosts structure and conversion scripts only. The original image archive is not supplied by this repository.
- PUI89 fit: **LOW/MEDIUM supplementary classification only.** Two states (raw/ripe) do not cover PUI89's four visible classes, and the source is not described as an on-tree crown/fruit detection dataset.
- Action: do not clone/download or install its requirements as part of this phase. Revisit only if the original archive can be lawfully accessed without cost and its image composition is confirmed.

### F. Mendeley Data — Coconut (matured and immatured)

- Source: https://data.mendeley.com/datasets/mmc345tfjw/1
- DOI: `10.17632/mmc345tfjw.1`
- Contributors shown: Dr Hemalatha Nambisan and Dr Rajesh M K; institutions shown: Aloysius Institute of Management and Information Technology and Central Plantation Crops Research Institute.
- Public description: data consists of matured and immatured coconuts.
- Licence displayed: CC BY 4.0.
- Availability evidence: the public page displays a **Download All** control, but does not describe the modality, image count, viewpoint, labels beyond the two terms, or file contents.
- PUI89 fit: **UNDETERMINED pending file inventory and sample inspection.**
- Action: keep in the candidate register; do not assume it contains usable RGB images until the archive contents are inspected.

## 4. Related sources excluded from the image training pool

- **Mendeley Tall Coconut Fruit Species acoustic signals:** acoustic rather than RGB image data. It is not part of the image dataset collection. It may be reconsidered as a separate future multimodal research stream only after modality-specific rights and sensor requirements are reviewed.
- **Coconut Tree Disease Dataset:** its public description concerns five disease categories, not the four maturity appearance classes. Do not mix disease images into the maturity labels. A separate disease-recognition scope would require its own task definition and review.
- Research papers that describe or cite the 400-image Mendeley crown dataset are evidence about the collection, not additional independent image sets. Do not double-count the same underlying source.

## 5. Licence and provenance rules

Before any candidate image is marked usable, record:

- exact source URL, DOI or dataset/version identifier;
- contributor/creator and publication date where supplied;
- licence name and a retained copy/link to the licence terms applicable to the source version;
- attribution/citation text required by the licence;
- whether commercial use, modification, redistribution and AI training are permitted under the applicable terms;
- any source-specific restrictions, third-party image notices, consent or privacy constraints;
- original filename, file size, image dimensions, file format and SHA-256 of original bytes;
- image-level source trace and any transformation history.

CC BY 4.0 requires attribution and notice of changes when applicable. Public Domain is recorded here as a platform-declared label, not as an independent legal finding. If the image-level origin or rights cannot be established, set `rights_status` to blocked/pending and exclude the image from training and redistribution.

Do not upload third-party image binaries into this repository during source discovery. Keep only source references, audit notes and later rights-cleared metadata. This avoids creating an unnecessary public redistribution copy and keeps the Git repository lightweight.

## 6. Collection and approval workflow

1. **Archive availability check:** confirm that the source's full archive can be obtained without payment, metered API, subscription or software installation. If access requires a paid service, stop and exclude it from this zero-cost collection phase.
2. **Archive inventory:** inspect filenames, file types, dimensions, counts, corrupt files, nested archives, annotation files and licence/attribution documents. Record observed counts; never copy the advertised count as an observed count.
3. **Image inspection:** visually inspect representative samples for real coconut fruit, on-tree versus off-tree context, tall palm/crown visibility, viewpoint, lighting, occlusion, image quality and non-coconut content.
4. **Duplicate and leakage audit:** compute SHA-256 and perceptual duplicate groups; compare overlapping Roboflow collections. Preserve orchard/tree/capture-session group identity where the source provides it. Do not invent missing group IDs.
5. **Class adjudication:** preserve original labels and create a separately versioned mapping only after two independent human reviewers and a documented adjudication rule. Ambiguous cases remain uncertain/review-required.
6. **Dataset gate:** populate the repository's metadata gate only with truthful records. The existing validator checks declared metadata and group isolation; it does not verify image pixels, copyright, consent or label truth.
7. **Training gate:** only rights-cleared, human-adjudicated, leakage-safe records may enter training/validation/test. Record the exact source version, manifest revision, code commit and evaluation environment.

## 7. Current status

| Gate | Status |
|---|---|
| Public source discovery | COMPLETE for the candidates listed here |
| Public-page licence label recorded | COMPLETE, subject to source-level verification |
| Creator/source attribution recorded | PARTIAL; some contributor details are sparse |
| Full archive actually downloaded | NOT STARTED |
| Archive file inventory | NOT STARTED |
| Image pixels inspected | NOT STARTED |
| Cross-source duplicate audit | NOT STARTED |
| Four-class mapping approved | NOT STARTED |
| Image-level rights/permission approval | NOT STARTED |
| Human annotation/adjudication | NOT STARTED |
| Training approval | BLOCKED |

**No images have been downloaded or copied into this repository by this audit. No software has been installed. No paid API, subscription, cloud GPU or metered service has been used. No training or model evaluation has been performed.**

## 8. Source references

- Mendeley Data, *Coconut tree crown*, DOI: https://doi.org/10.17632/w4t73tvrf8.1
- Roboflow Universe, *On-tree mature coconut fruit detection*: https://universe.roboflow.com/college-if44x/on-tree-mature-coconut-fruit-detection
- Roboflow Universe, *On tree mature coconut fruit detection using SOLOv2*: https://universe.roboflow.com/college-if44x/on-tree-mature-coconut-fruit-detection-using-solov2
- Roboflow Universe, *Coconut_maturity_Classification*: https://universe.roboflow.com/tejaswini-d-tjrmk/coconut_maturity_classification
- RawRipe repository and README: https://github.com/ai-agriculture-circuits-and-systems/RawRipe
- Mendeley Data, *Coconut*, DOI: https://doi.org/10.17632/mmc345tfjw.1

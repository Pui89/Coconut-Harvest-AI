# PUI89 Coconut Harvest AI — Dataset Archive Access Review v1.0

**Review date:** 2026-11-23  
**Related source audit:** `docs/COCONUT_OPEN_DATASET_SOURCE_AUDIT_V1.0.md`  
**Status:** PUBLIC DOWNLOAD PATHS IDENTIFIED; ARCHIVE CONTENTS NOT YET RETRIEVED OR INSPECTED

## 1. Decision

This stage verifies how the candidate datasets may be obtained. It does not download or mirror image files.

**No archive has been downloaded.** No account has been created, no API key requested, no package installed, and no paid plan or metered service used.

## 2. Access review by source

### Mendeley — Coconut tree crown (DOI 10.17632/w4t73tvrf8.1)

- Page: https://data.mendeley.com/datasets/w4t73tvrf8/1
- The public page exposes a **Download All** control and identifies version 1, 400 RGB images (512 × 512), and CC BY 4.0.
- The rendered Files section does not enumerate individual filenames.
- Mendeley Data API documentation describes public dataset metadata, public file-list and ZIP endpoints, and download redirects. The API documentation describes OAuth2 authentication for API operations. No API client was registered, token requested, authenticated endpoint called, or archive download tested.
- **Status:** browser download control visible; successful retrieval, archive size, file list and checksum UNVERIFIED.
- **Next:** use the public page's Download All control only if it offers a direct no-cost browser download without account/API setup. Stop if login, API registration, payment or other unexpected conditions are required.

### Mendeley — Coconut (DOI 10.17632/mmc345tfjw.1)

- Page: https://data.mendeley.com/datasets/mmc345tfjw/1
- The public page exposes **Download All**, version 1, matured/immatured coconut description and CC BY 4.0.
- It does not state image count, file formats, viewpoint or whether files are RGB photographs.
- **Status:** browser control visible; archive retrieval and modality UNVERIFIED.
- **Next:** inspect only through a no-cost browser download. Do not treat as an image source until file inventory confirms image files.

### Roboflow — On-tree mature coconut fruit detection (college; 268 images)

- Project: https://universe.roboflow.com/college-if44x/on-tree-mature-coconut-fruit-detection
- Version page: https://universe.roboflow.com/college-if44x/on-tree-mature-coconut-fruit-detection/dataset/1
- The public page exposes the dataset version and image gallery. Roboflow's documented Universe workflow is to open the dataset version, choose **Download Dataset**, then choose ZIP or download code. The project landing-page licence applies.
- The page's inference examples require an API key and package installation. These are for model inference, **not required steps for a manual ZIP export**, and are out of scope.
- **Status:** export workflow documented; actual ZIP availability, login requirement, format options and free-plan limits NOT TESTED.
- **Next:** check for a no-cost public browser ZIP export only. Do not create an account/workspace, generate API keys, fork to a workspace, install packages or start hosted training.

### Roboflow — On-tree mature coconut fruit detection using SOLOv2 (college; 495 images, two versions)

- Project: https://universe.roboflow.com/college-if44x/on-tree-mature-coconut-fruit-detection-using-solov2
- Version page: https://universe.roboflow.com/college-if44x/on-tree-mature-coconut-fruit-detection-using-solov2/dataset/1
- Same documented Universe export workflow. Same displayed contributor and stage labels as the 268-image project; source-image overlap is possible.
- **Status:** export workflow documented; actual ZIP availability, login requirement, format options and free-plan limits NOT TESTED.
- **Next:** only no-cost public browser export; compare hashes and image content against the other college dataset before combining.

### Roboflow — Coconut_maturity_Classification (Tejaswini D; 3,826 images, version 3)

- Project: https://universe.roboflow.com/tejaswini-d-tjrmk/coconut_maturity_classification
- Version page: https://universe.roboflow.com/tejaswini-d-tjrmk/coconut_maturity_classification/dataset/3
- Same documented Universe export workflow. Public page identifies CC BY 4.0 and six classification labels.
- Hosted-model/API examples require an API key and package installation; they are not needed for manual ZIP export and are out of scope.
- **Status:** export workflow documented; actual ZIP availability, login requirement, format options and free-plan limits NOT TESTED.
- **Next:** only no-cost public browser export. Check on-tree/off-tree context; preserve original labels and do not use displayed model accuracy as PUI89 benchmark evidence.

### RawRipe

- Repository: https://github.com/ai-agriculture-circuits-and-systems/RawRipe
- Its README states that the original dataset is available through IEEE Xplore and that this GitHub repository hosts structure and conversion scripts, not the original archive.
- README states 150 coconut images (raw 72, ripe 78), RGB image-level classification and CC BY 4.0. It says images were collected from search engines and agricultural sources.
- **Status:** original image archive not hosted in this repository; IEEE Xplore access/download conditions unverified.
- **Decision:** exclude from immediate retrieval unless the original archive can be lawfully accessed at no cost. Do not install requirements or run conversion scripts.

## 3. Access and cost controls

- Public visibility does not guarantee direct download, account-free access or unrestricted export.
- Do not create accounts, register API clients, generate API keys, install packages, use hosted inference, fork datasets into a cloud workspace or start training without separate explicit approval.
- Do not use paid plans, trials that convert to paid, metered APIs, cloud GPUs or other chargeable services.
- Do not copy third-party image archives into this GitHub repository. Keep source references, licence/attribution records, metadata manifests and audit results only unless a separate redistribution review authorizes otherwise.
- If a source requires login, API credentials, account creation or payment, stop and report the exact requirement. Do not bypass access controls.
- Once an archive is lawfully obtained, record original archive SHA-256, size, retrieval date, dataset/version, file inventory and licence/attribution files before extraction or transformation.

## 4. Corrected technical observations

- Mendeley crown: 400 RGB 512 × 512 upward-looking crown images; no four-class per-fruit labels stated in public description.
- Mendeley Coconut: modality and image count unknown; do not assume it is an image collection.
- Roboflow college collections: separate pages, same contributor and similar stage labels; counts must not be summed as unique samples before duplicate analysis.
- RawRipe: 150 coconut samples (72 raw, 78 ripe); classification only, not on-tree detection. Its README explicitly describes search-engine/agricultural-source image collection and says the original archive is on IEEE Xplore.
- Roboflow hosted-model metrics are third-party model page values, not independent PUI89 validation.

## 5. Gate status

| Gate | Status |
|---|---|
| Public dataset pages revisited | COMPLETE |
| Download/export procedure identified | PARTIAL |
| Direct account-free archive download tested | NOT TESTED |
| Archive downloaded | NOT STARTED |
| Archive SHA-256 / size recorded | NOT STARTED |
| Actual file inventory | NOT STARTED |
| Sample images visually inspected | NOT STARTED |
| Image-level rights/provenance confirmed | NOT STARTED |
| Duplicate/overlap analysis | NOT STARTED |
| PUI89 four-class mapping | NOT STARTED |
| Training approval | BLOCKED |

**This is access research only. No dataset archive was retrieved and no image is approved for training.**

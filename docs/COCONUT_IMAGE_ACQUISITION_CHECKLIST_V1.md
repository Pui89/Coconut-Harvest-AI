# Coconut Image Acquisition & Integrity Checklist v1

**Review date:** 17 November 2026
**Scope:** WMC-01 and WMC-02 only.
**Status:** Source-page and original-image-link inspection completed in browser; local original-file acquisition and byte-level integrity verification remain blocked.

## 1. Verified source metadata

| ID | Original file | Dimensions | Commons file size | Creator | License |
|---|---|---:|---:|---|---|
| WMC-01 | Coconut_in_Coconut_Tree.jpg | 5,184 × 3,456 | 8.23 MB (8,631,989 bytes) | Sarmi~Kili | CC BY-SA 4.0 |
| WMC-02 | Mature_Coconut_Palm_with_Coconuts_(Cocos_nucifera).jpg | 3,072 × 4,096 | 4.68 MB | Johnnybam | CC BY-SA 4.0 |

Source pages:
- WMC-01: https://commons.wikimedia.org/wiki/File:Coconut_in_Coconut_Tree.jpg
- WMC-02: https://commons.wikimedia.org/wiki/File:Mature_Coconut_Palm_with_Coconuts_(Cocos_nucifera).jpg

Original-file links opened from the Commons source pages:
- WMC-01: https://upload.wikimedia.org/wikipedia/commons/b/be/Coconut_in_Coconut_Tree.jpg
- WMC-02: https://upload.wikimedia.org/wikipedia/commons/e/e8/Mature_Coconut_Palm_with_Coconuts_(Cocos_nucifera).jpg

Both source pages display CC BY-SA 4.0. Reuse requires appropriate creator credit, a link to the license, indication of changes, and compliance with ShareAlike for adapted material. This record is not legal advice or independent verification of uploader rights.

## 2. Original-image visual observations

- WMC-01 original-image link displayed at 5,184 × 3,456. Multiple coconuts are visible around the crown. Several fruit are partially hidden by fronds, stems, or neighbouring fruit. Strong sunlight and bright background gaps create varied illumination. Candidate for canopy detection and occlusion testing.
- WMC-02 original-image link displayed at 3,072 × 4,096. A dense cluster of green to yellow-green fruits is visible against the trunk and foliage. Some fruit boundaries overlap; several are partly hidden. Candidate for canopy detection, but individual instance boundaries need careful annotation.
- These are visual observations only. No maturity class is assigned. Source captions do not independently establish biological maturity.

## 3. Acquisition attempt and integrity status

| Check | WMC-01 | WMC-02 |
|---|---|---|
| Source page opened | pass | pass |
| Original link opened in browser | pass | pass |
| Original dimensions shown by source | pass | pass |
| Original file downloaded to local working storage | blocked / failed | blocked / failed |
| Local byte size measured | pending | pending |
| Local SHA-256 computed | pending | pending |
| File decodes locally and dimensions verified | pending | pending |
| File retained unchanged | pending | pending |

Download attempts through the available file-transfer path failed. Therefore no claim is made that original image bytes are present in local storage. Browser display of an original-file link is not equivalent to acquiring and hashing the file.

## 4. Required completion steps

1. Acquire the exact original bytes from the listed upload.wikimedia.org URL using an approved download path.
2. Preserve the original filename; do not resize, recompress, crop, or edit the source file.
3. Record local byte size and SHA-256; compare byte size and dimensions with source metadata.
4. Decode the file locally and verify JPEG integrity and dimensions.
5. Keep the source file outside the public Git repository unless a separate, explicit publication decision is made.
6. Record acquisition timestamp, source URL, tool/method, result, and reviewer.
7. Only after integrity verification, proceed to human bounding-box annotation and independent QA.

## 5. Current dataset gate

- WMC-01 and WMC-02 remain candidate-only.
- Detection annotation: not started.
- Biological maturity: unknown.
- Independent annotation QA: not started.
- Training/evaluation approval: false.
- No image bytes were committed to the repository and no model was trained.
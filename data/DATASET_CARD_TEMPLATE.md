# Dataset Card Template — Coconut Harvest AI

Copy this file for each proposed image or sensor dataset. Complete it before using the data for training, tuning, evaluation, or public release.

> **Gate:** If ownership, permission/licence, provenance, or intended use is unknown, mark the dataset **BLOCKED — NOT FOR TRAINING OR REDISTRIBUTION**. Do not infer permission from a public download link.

## 1. Identity and intended use

- Dataset name:
- Dataset version:
- Record owner / responsible reviewer:
- Date prepared (UTC):
- Intended use: [ ] development  [ ] training  [ ] validation  [ ] held-out evaluation  [ ] demonstration only
- Data modalities: [ ] RGB  [ ] depth  [ ] thermal/NIR  [ ] LiDAR  [ ] other:
- Geographic / cultivar / growing context, if known:
- Intended claims this dataset can support:
- Claims it cannot support:

## 2. Provenance, rights, and restrictions

- Original source or collection method:
- Source URL or private record reference (do not expose private URLs/tokens):
- Collection / download date (UTC):
- Rights holder:
- Exact licence or written permission reference:
- Commercial use permitted? [ ] yes  [ ] no  [ ] unclear
- Modification / annotation permitted? [ ] yes  [ ] no  [ ] unclear
- Redistribution permitted? [ ] yes  [ ] no  [ ] unclear
- Attribution / share-alike / other conditions:
- Personal data, identifiable people, property, or sensitive location data present?
- Required consent, privacy, retention, or deletion controls:
- Rights review status: [ ] approved for stated use  [ ] blocked  [ ] pending
- Reviewer and review date:

**Do not commit restricted source images, credentials, private location data, or data that the project is not permitted to redistribute.** A licence for code does not automatically license a dataset.

## 3. Inventory and integrity

- Number of original images / scenes:
- Number excluded and reason:
- File formats and resolution range:
- Duplicate / near-duplicate check method and result:
- Corrupt / unreadable files:
- Integrity manifest location (for example, SHA-256 hashes; never include secrets):
- Known gaps or collection bias:

## 4. Annotation protocol and quality

- Label schema and version:
- Operational definitions for young green, mature green, brown/dry, damaged, occluded, and uncertain:
- Annotation tool and version:
- Annotator(s) or role identifiers:
- Review procedure and adjudication method:
- Handling of occlusion, truncation, mixed-stage bunches, and ambiguous cases:
- Inter-annotator agreement, if measured:
- Known label errors / unresolved disputes:
- Annotation status: [ ] draft  [ ] reviewed  [ ] approved for stated split

Do not silently convert uncertain or disputed labels into ground truth. Keep an audit trail for corrections.

## 5. Leakage-resistant split

- Split policy and rationale:
- Group key used to keep related data together (e.g., tree, orchard, capture session, video sequence):
- Train / validation / test counts:
- Evidence that near-duplicates and related frames do not cross splits:
- Held-out test set access policy:
- Split file and version:

Prefer splitting by tree, site, or capture session rather than randomly splitting neighbouring frames or near-identical images. Record any limitation that prevents a truly independent test.

## 6. Evaluation linkage

- Code commit:
- Model / checkpoint version:
- Evaluation command:
- Metrics and exact definitions:
- Confidence / IoU thresholds:
- Per-class results and failure categories:
- Environment and random seed:
- Raw report path:
- Human reviewer:
- Known limitations:

A metadata validator passing means only that required report fields are structurally complete. It does **not** prove label quality, scientific validity, real-orchard generalization, safe robot operation, or successful harvesting.

## 7. Release decision

- Decision: [ ] approved for stated use  [ ] restricted  [ ] blocked
- Approved uses:
- Prohibited uses:
- Required attribution:
- Conditions before external sharing:
- Reviewer:
- Date (UTC):
- Next review trigger (e.g., new source, licence change, new intended use, or annotation revision):

---

## Minimal checklist

- [ ] Source and collection method recorded.
- [ ] Exact licence or permission checked for the intended use.
- [ ] Privacy and redistribution restrictions reviewed.
- [ ] Annotation definitions and review status recorded.
- [ ] Related images grouped to prevent split leakage.
- [ ] Dataset version and integrity information recorded.
- [ ] Held-out evaluation data kept separate from tuning.
- [ ] Public claims match the evidence and limitations.

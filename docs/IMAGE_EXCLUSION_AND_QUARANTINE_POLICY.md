# Coconut Image Exclusion and Quarantine Policy

**Purpose:** keep the dataset scientifically defensible without hiding difficult examples or deleting audit history.

## Decision categories

| Category | Examples | Dataset action | Keep in audit record? |
|---|---|---|---|
| Reject as unusable | Corrupt/unreadable file, unrelated subject, irrecoverably tiny image | Exclude from active dataset | Yes; record reason and file hash when available |
| Quarantine — rights unresolved | Missing source page, creator, licence, or attribution details | Do not train on, publish, or redistribute until checked | Yes |
| Quarantine — annotation unresolved | Fruit boundaries or labels cannot be agreed, boxes may be wrong, hidden fruit is guessed | Exclude from training and scored evaluation until independently reviewed | Yes |
| Challenge set | Genuine but dark, blurry, occluded, cluttered, or unusual orchard conditions | Keep separate from the primary benchmark; use only with documented labels and purpose | Yes |
| Model failure | A valid, eligible image on which the model misses fruit or produces false detections | Keep in evaluation; document the failure | Yes |
| Approved candidate | Rights and attribution checked, image integrity checked, labels independently reviewed, split/group assigned | Eligible for the frozen dataset after all QA gates pass | Yes |

## Rules

1. **Never exclude an image solely because the model performs poorly on it.** That would bias evaluation and inflate apparent performance.
2. **Do not call an image “weak” based only on one subjective impression.** Record a concrete reason, such as severe blur, unusable resolution, irrelevance, unresolved rights, or annotation ambiguity.
3. **Quarantine rather than silently delete** any candidate with unresolved rights or labels. Keep source records, file hashes, and the exclusion reason so decisions can be audited.
4. **Separate training, validation, primary test, and challenge sets.** Freeze the primary test set before tuning; group images by source, tree, scene, or capture session to reduce leakage.
5. **Do not count concept artwork, synthetic examples, or manual-review photographs as detector-performance evidence.** Report the evidence type explicitly.
6. **Promote an image only after the relevant gates pass:** integrity, source/licence/attribution review, annotation QA, duplicate/leakage checks, and split assignment.
7. **Keep a decision log.** For every excluded or quarantined image, record candidate ID, filename, reason code, reviewer/date, and whether the decision can be revisited.

## Current known decisions

- Candidates **0002** and **0004** have first-pass boxes archived because annotation QA is unresolved. They are **not for training**. Preserve the archive as audit history; do not present their failed HSV smoke-test score as a learned-model result.
- Candidate **0033** is deferred for difficult shadows, glare, and frond occlusion; it may be useful as a challenge example after review.
- Candidate **0034** is a labeling candidate with substantial overlap and partial occlusion. Annotate only clearly distinguishable fruit and request a second review; do not guess hidden fruit.
- Candidate **0031** is deferred because of severe backlighting.
- Candidate **0032** is a labeling priority, not yet training-approved.
- Any candidate whose source rights have not been independently checked remains blocked from the approved training set, regardless of visual quality.

## Reporting template

For each dataset release, report:

- total candidates reviewed;
- approved, rejected, and quarantined counts with reason codes;
- rights-clearance and independent-annotation-review status;
- duplicate and split-leakage checks;
- the frozen split manifest/version;
- performance on the untouched primary test set and any separately reported challenge set;
- known limitations and unresolved items.

**Important:** exclusion policy improves dataset governance; it does not itself improve detector accuracy. Any performance claim must come from a reproducible evaluation on appropriately reviewed data.

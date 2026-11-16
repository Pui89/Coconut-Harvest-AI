# Coconut Real-Image Test Set v1

**Status:** implemented as a discovery and human-review register; not a training dataset.  
**Created:** 16 November 2026  
**Image files downloaded or committed by this change:** 0  
**New labels approved by this change:** 0  
**Training-approved images added by this change:** 0

## Purpose

Create one reviewable starting point for real coconut photographs, recording where each candidate came from, the licence shown on its source page, attribution requirements, image-file evidence, and the human checks needed before any model evaluation.

This v1 is deliberately a **candidate register**, not a claim that the four classes are represented or that any image is cleared for training. The CSV companion is `../data/coconut_real_image_test_set_v1.csv`.

## Project label policy

Keep the four PUI89 operational visual classes separate:

- `young_green`
- `mature_green`
- `yellow`
- `brown`

Also allow `unknown`, `uncertain`, and `ignore`. Record visible husk colour separately from biological maturity. Do not infer biological maturity from colour alone: cultivar, fruit age, intended harvest use, fruit development, and postharvest drying can change the interpretation. A qualified coconut/agronomy reviewer must confirm the class policy for the target cultivar and use case.

## Candidate image register

The machine-readable records are in the companion CSV. The five source-page candidates below were already identified in the project's four-stage source register; this v1 links them into one review queue rather than downloading duplicate files.

| Record | Source | Creator | Licence displayed in source register | Initial review purpose |
|---|---|---|---|---|
| WMC-01 | [Coconut in Coconut Tree.jpg](https://commons.wikimedia.org/wiki/File:Coconut_in_Coconut_Tree.jpg) | Sarmi~Kili | CC BY-SA 4.0 | Attached green-looking fruit; canopy/occlusion; existing project candidate 0032 |
| WMC-02 | [Mature Coconut Palm with Coconuts](https://commons.wikimedia.org/wiki/File:Mature_Coconut_Palm_with_Coconuts_%28Cocos_nucifera%29.jpg) | Johnnybam | CC BY-SA 4.0 | Mature-palm context; inspect individual fruit and visible husk |
| WMC-03 | [Coconut Yellow Gourigatram.jpg](https://commons.wikimedia.org/wiki/File:Coconut_Yellow_Gourigatram.jpg) | Giri1234 | Public domain, as stated by uploader | Yellow-coloured cultivar reference; not evidence of biological maturity |
| WMC-04 | [Coconut Yellow.JPG](https://commons.wikimedia.org/wiki/File:Coconut_Yellow.JPG) | Iaminfo | CC BY-SA 3.0 (GFDL also offered) | Yellow-husk appearance and cultivar variation |
| WMC-05 | [The fruit of coconut.jpg](https://commons.wikimedia.org/wiki/File:The_fruit_of_coconut.jpg) | Lotadegbemijowa | CC BY-SA 4.0 | Brown/ripened plucked-fruit appearance; out-of-domain for canopy detection unless separately tagged |

**Licence caution:** these are source-page licence statements copied from the existing project research register, not legal approvals. Re-open every source page before acquisition or redistribution; verify the exact file revision, creator, licence, attribution, and any ShareAlike obligations. Public availability is not permission by itself.

## Review fields and workflow

For every candidate, complete the CSV fields as evidence becomes available:

1. **Source and rights:** source page, creator, exact licence and licence URL, attribution, source-page review date, rights reviewer and explicit decision.
2. **Original file:** unchanged original filename, download status, dimensions, byte size, SHA-256, and local file location. Do not commit image bytes to the public repository by default.
3. **Domain suitability:** attached-to-palm, harvested, close-up, market, or other; assess visibility, blur, occlusion, lighting, and whether individual fruit boundaries can be annotated.
4. **Labels:** visible husk colour and biological maturity are separate fields. Record the proposed class, rationale, reviewer, and confidence/evidence. Use unknown/uncertain/ignore when ambiguous.
5. **Annotation QA:** preserve initial labels, independent reviewer decision, adjudication, and annotation version. Never silently overwrite disagreement.
6. **Evaluation split:** group by orchard, tree, source, and capture session before assigning train/validation/test. Keep an independent test split frozen and prevent related or near-duplicate images crossing splits.

Use the existing [human-review checklist](COCONUT_IMAGE_HUMAN_REVIEW_CHECKLIST.md), [four-stage source register](COCONUT_FOUR_STAGE_IMAGE_SOURCE_REGISTER.md), and [fail-closed dataset promotion gate](COCONUT_DATASET_PROMOTION_GATE.md). The existing rights and candidate-review ledgers remain authoritative for promotion; this discovery CSV does not replace them or approve any record.

## Training and evaluation gate

An image may enter a model-evaluation set only after all applicable checks are evidenced:

- exact source and licence reviewed for the intended use;
- attribution and share-alike obligations recorded;
- original file identity and SHA-256 verified;
- image is suitable for the stated detection/classification task;
- annotations reviewed at native resolution by a human;
- maturity label independently reviewed, with expert adjudication where needed;
- duplicate and source/tree/session leakage checks passed;
- record is explicitly approved in the canonical rights and candidate-review ledgers.

Until then, keep rights, annotation, and training approval states pending/false. Do not run training, publish model accuracy, or describe this as a validated test set. When the checks are complete, run the existing promotion gate and the repository's dataset preflight and held-out benchmark workflow.

## Current v1 outcome

- Candidate source records listed: **5**.
- Existing candidate 0032 cross-reference: **1**.
- New image files downloaded: **0**.
- New annotations or maturity labels approved: **0**.
- New images approved for training/testing: **0**.
- Model evaluation performed by this change: **No**.

This is a structured, auditable preparation step only. It does not establish image rights, annotation correctness, four-class coverage, detector performance, or field capability.

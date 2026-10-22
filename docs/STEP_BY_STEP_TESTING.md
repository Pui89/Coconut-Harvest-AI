# Step-by-Step Testing Guide

This guide is a practical test sequence for contributors and the project owner. Use free tools already in the repository; do not upload private data or install paid services.

## 1. Check the current commit
- Open the repository's **Actions** tab.
- Open the latest run for the commit you want to assess.
- Record the commit SHA and distinguish **success**, **failure**, **cancelled**, and **in progress**.

## 2. Run software checks
From a local clone, open a terminal in the repository root and use the test command documented in the repository's workflow. If the Python test workflow uses pytest and dependencies are installed, run:
```powershell
python -m pytest
```
If it fails, save the complete error and fix the first underlying error before rerunning. A passing unit test verifies software logic only.

## 3. Check the annotation data
- Confirm every referenced image exists and opens.
- Validate annotation JSON schema and ensure normalized box coordinates are within [0, 1], with positive width and height.
- Review boxes visually for missed coconuts, false boxes, occlusion and duplicates.
- Check the source manifest and license/permission conditions for each image.
- Keep AI-generated boxes labelled as drafts until a human approves them. Do not train or score a benchmark against unreviewed draft labels.

## 4. Check model evaluation readiness
Before reporting precision, recall, F1, IoU/mAP or latency, record the model/checkpoint, dataset version, approved ground truth, split manifest, confidence threshold, hardware and exact command. Prevent images from the same source/scene leaking across train and test splits.

## 5. Test safety logic
Exercise low-confidence detection, missing depth, unreachable targets, obstacle blockage, and missing human approval. Each should fail safe and must not command an arm or cutter.

## 6. Record the result
Create a dated report with commit SHA, commands, pass/fail/not-run status, sample counts, failures and limitations. Never invent model metrics or describe software tests as proof of orchard readiness.

## Current known follow-up
The candidate-image fetch has encountered Wikimedia HTTP 429 rate limits. Treat the candidate set as incomplete until the manifest confirms the expected files; preserve partial-download provenance and retry later rather than claiming all candidates were fetched.

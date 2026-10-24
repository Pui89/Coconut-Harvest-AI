# PUI89 Shared Engineering Standard — Coconut Harvest AI

**Purpose:** make development repeatable, low-cost, reviewable, and evidence-led. This document records a working standard; it does not claim new tests or model results have been run.

## Operating rules

1. **Free-first:** prefer local tools and GitHub Actions within available free quotas. Do not add paid APIs, hosted GPUs, subscriptions, or services that can incur charges without explicit approval.
2. **Inspect before changing:** read the existing implementation and tests first. Avoid duplicating utilities already in the repository.
3. **Small, reviewable changes:** isolate changes, explain the reason, add regression tests, and use a pull request when practical.
4. **Evidence over claims:** label work as implemented, tested, measured, proposed, or blocked. A passing software test does not prove field performance.
5. **Reproducibility:** record commands, dependency versions, dataset/split identifiers, model/checkpoint identity, and relevant configuration for experiments.

## Project-specific priority: unblock trustworthy coconut evaluation

The latest dataset-readiness snapshot reports 34 candidate records and 0 approved for training. Keep the gate closed until the actual source, license/permission, attribution, annotation quality, and approval requirements are satisfied.

Recommended sequence:

1. Review source-page terms and attribution for each candidate; public availability alone is not permission.
2. Annotate only clearly visible fruit and preserve an explicit review status for uncertain examples.
3. Run annotation geometry and overlay checks; have a separate reviewer inspect labels.
4. Group data by orchard/source/session before splitting, then audit exact and near duplicates across splits.
5. Freeze a held-out test set before tuning.
6. Run a named compatible detector and publish actual precision, recall, F1/mAP as appropriate, per-condition errors, latency, sample count, hardware, and command/configuration.
7. Do not claim maturity classification, 0–30 m reach, safe cutting, or successful physical harvesting without separate evidence.

## Shared quality gates

- Run the existing lightweight unit tests and CI workflow.
- Keep data validation separate from legal/visual human review.
- Do not silently promote candidate data when automated structure checks pass.
- Treat example outputs and smoke tests as pipeline checks, not real-world model performance.
- Record failures and limitations alongside successful results.

## Definition of done

A change is complete only when its code/docs are reviewed, relevant automated checks have actually run, the result is reported accurately, and any remaining limitation is explicit. If a check has not run, mark it **not verified**.

## Immediate next action

Work through the repository's dataset readiness and first real-image benchmark checklists. Do not spend compute on training until there is a lawful, human-reviewed dataset and a frozen evaluation plan.

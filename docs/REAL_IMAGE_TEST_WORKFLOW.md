# Real Coconut Image Review — Zero-Cost Workflow

## Purpose and current status

This workflow adds real photographs to the **human review and data-preparation stage**. It does not yet detect coconuts automatically. The existing `agents/harvest_planning_agent.py` accepts candidate records; it does not inspect image pixels.

The sample photos are fetched from Wikimedia Commons only when you run the download command. They are not committed to this repository. The repository references these images as CC0 1.0; always check the live source page and licence before reusing or redistributing a file.

## Requirements

- Windows 11 and Python already installed (the user's reported Python 3.14.5 is suitable for this standard-library helper).
- Internet connection only for the optional photo download.
- No `pip install`, API key, model download, paid API, subscription, cloud GPU, or new hardware.

## Run it

Open Command Prompt in the repository folder `Coconut-Harvest-AI-main` and run:

```bat
python scripts/prepare_real_image_review.py --download
```

The script creates:

- `data/real_image_samples/fruiting_coconut_palm_canopy.jpg`
- `data/real_image_samples/coconut_plucker_harvesting.jpg`
- `data/real_image_samples/image_review.csv`
- `data/real_image_samples/SOURCES.md`

The images and review CSV are local working data and are not uploaded to GitHub automatically.

## Review the real photographs

1. Open the two `.jpg` files using Photos or Paint.
2. For each image, manually record visible coconut count, partly hidden/occluded count, lighting, background clutter, and notes in `image_review.csv`.
3. Do not label a guessed 3D position, robot reachability, or detector confidence from a normal RGB photo. Leave those unknown unless a suitable sensor/model or independent measurement supplies them.
4. Keep human annotations separate from model predictions. Record uncertain or uncountable targets as uncertain rather than inventing a precise label.

## What this test can establish

After completing the CSV, you will have a small, manually reviewed real-image sample and a record of visual challenges. This is a **manual image review**, not an AI benchmark and not a detector test. Two photographs are only a workflow smoke test, not enough data for scientific claims.

The existing rule-based agent can only make a proposal when candidate records contain its required fields. Real RGB photographs alone do not provide calibrated 3D coordinates or verified reachability. Do not convert image observations into invented 3D values just to make the agent select a target. The safe next stage is to add a separately evaluated detector and, later, measured depth/reachability inputs.

## Source and licence notes

- [Fruiting Coconut Palm Canopy — source page](https://commons.wikimedia.org/wiki/File:Fruiting_Coconut_Palm_Canopy.jpg)
- [Coconut Plucker plucking coconuts on a tree in Mumbai — source page](https://commons.wikimedia.org/wiki/File:Coconut_Plucker_plucking_coconuts_on_a_tree_in_Mumbai..JPG)
- [CC0 1.0 legal code](https://creativecommons.org/publicdomain/zero/1.0/)

The original source pages are authoritative for creator and licence information. The script writes a local source manifest as well. If a URL changes or a download fails, open the source page directly and download the image manually; do not bypass attribution or licence requirements.

## Research reporting template

Once reviewed, report only what was actually recorded:

- Images reviewed: number of downloaded and successfully opened files.
- Manual count annotations: number of images with completed count fields.
- Visual conditions observed: lighting, occlusion, and background clutter noted by the reviewer.
- AI detector metrics: **not measured by this workflow**.
- Robot reachability and collision safety: **not measured by this workflow**.


## Validate the completed review CSV

After editing the CSV, run this optional local checker from the repository root:

```bat
python scripts/validate_real_image_review.py
```

The checker verifies that the expected columns exist, image files are present beside the CSV, and annotation fields are filled. If a count cannot be determined, leave it blank and explicitly explain the uncertainty in `review_notes` (for example, `uncertain count due to occlusion`). It uses Python's standard library only.

A passing result means the annotation CSV passed basic data-quality checks. It does **not** measure AI detection accuracy, infer depth, confirm reachability, or authorize robot motion.

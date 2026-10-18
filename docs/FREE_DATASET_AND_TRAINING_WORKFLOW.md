# Free dataset and reproducible detector workflow

## What was found

A public GitHub repository called [coconut-annotations](https://github.com/adriannebulao/coconut-annotations) describes annotations for on-tree clustered coconut detection, but its README says the image files must be obtained separately. The reviewed files do not provide a clear dataset licence, so it is **not yet cleared for training or redistribution**.

Other search results included dataset-listing repositories that say full data files require sponsorship; those are not treated as free datasets. A public fruit maturity dataset called [RawRipe](https://github.com/ai-agriculture-circuits-and-systems/RawRipe) describes only image-level/full-image boxes for its coconut category, so it is not suitable for precise coconut fruit boxes in an orchard canopy.

I did not verify a complete, directly downloadable, clearly licensed, non-Roboflow orchard object-detection dataset. In line with this project's no-Roboflow/no-paid-service rule, no external dataset has been imported and no images have been copied into this repository.

## Safest free route

- Collect your own orchard photographs/video frames where you have permission, or obtain written permission from a researcher/farm.
- Label every coconut with a tight bounding box; include representative negative images and difficult cases such as leaves, glare, shade, small/far fruit, and overlapping bunches.
- Record image source, collection date/session, camera, and permission/licence.
- Split by tree, location, or video session into train/validation/test so near-identical frames cannot leak across splits.
- Keep all source images and model weights local and outside Git.
- Train and evaluate using the scripts in [training/README.md](../training/README.md).

## Free tooling and cost boundary

The code uses local Python packages and local computation. It does not require a hosted inference endpoint, paid notebook, cloud GPU, or subscription. A compatible local base checkpoint is still needed and must be obtained manually after reviewing its licence. Downloading a checkpoint uses internet data and disk space. Ultralytics package/model licensing should be reviewed before commercial distribution.

## Current evidence status

- Training/evaluation scripts: repository code, not yet run against a verified real dataset.
- Trained coconut weights: not included or claimed to exist.
- Test metrics: none reported until a frozen, labelled test split is evaluated.
- Robot integration: existing RGB-D pipeline can consume local coconut weights and produce a JSON review proposal; it cannot command hardware and fails closed when required spatial evidence is missing.

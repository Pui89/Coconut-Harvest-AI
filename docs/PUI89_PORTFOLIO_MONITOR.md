# PUI89 Portfolio Monitor

A scheduled, read-only status snapshot for the three public PUI89 project repositories:

- Coconut Harvest AI
- Extreme Flood Rescue AI
- Multimodal Narcotics Screening AI

## Operation

The GitHub Actions workflow runs daily at 02:00 UTC (approximately 09:00 Thailand time), on manual dispatch, and when the monitor itself changes on `main`. It queries public GitHub repository metadata, recent Actions runs, and open pull requests. It produces JSON and Markdown files and uploads them as a 30-day Actions artifact.

## Cost and permissions

- Python standard library only; no third-party packages, paid APIs, cloud GPU, or external secrets.
- Read-only GitHub workflow permissions.
- No repository writes, commits, merges, deployments, model downloads, or hardware commands.
- Public GitHub API rate limits and scheduled-run delays may affect freshness.

## Evidence boundary

A successful monitor means the snapshot was collected. It does not mean every project check passed. Workflow results are reported as workflow evidence only; they do not prove AI accuracy, dataset suitability, simulation validity, or physical robot safety. Cancelled and skipped runs are not treated as failures. Retrieval errors are marked as partial rather than silently converted to success.

## Retrieve a report

Open the repository's **Actions → PUI89 Portfolio Monitor**, select a completed run, and download the `pui89-portfolio-status-*` artifact.

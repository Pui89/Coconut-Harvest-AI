[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$DatasetRoot,
    [Parameter(Mandatory = $true)]
    [string]$LocalCheckpoint,
    [string]$ExperimentId = "coconut-baseline-v1",
    [int]$Epochs = 30,
    [int]$ImageSize = 416,
    [string]$Device = "0"
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path -LiteralPath $DatasetRoot).Path
$dataYaml = Join-Path $root "coconut.yaml"
$checkpoint = (Resolve-Path -LiteralPath $LocalCheckpoint).Path
if (-not (Test-Path -LiteralPath $dataYaml -PathType Leaf)) {
    throw "Dataset YAML not found: $dataYaml"
}
if (-not (Test-Path -LiteralPath $checkpoint -PathType Leaf)) {
    throw "Local checkpoint not found: $checkpoint. This script never downloads model weights."
}
if ($Epochs -lt 1 -or $ImageSize -lt 128) {
    throw "Epochs must be positive and ImageSize must be at least 128."
}

function Invoke-PythonStep {
    param([string[]]$PythonArgs)
    Write-Host ([Environment]::NewLine + "> python " + ($PythonArgs -join " ")) -ForegroundColor Cyan
    & python @PythonArgs
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code $LASTEXITCODE"
    }
}

$reports = Join-Path (Get-Location) "reports"
New-Item -ItemType Directory -Force -Path $reports | Out-Null
$runName = $ExperimentId
$bestWeights = Join-Path (Get-Location) "runs\coconut\$runName\weights\best.pt"
$testReport = Join-Path $reports "$ExperimentId-test-report.json"
$manifest = Join-Path $reports "$ExperimentId-test-manifest.json"
$audit = Join-Path $reports "$ExperimentId-provenance-audit.json"

Write-Host "This runs locally. It does not download a dataset, install packages, or download model weights." -ForegroundColor Yellow
Write-Host "A successful run is not proof of performance outside this held-out dataset."
Invoke-PythonStep @("training/check_dataset.py", "--root", $root)
Invoke-PythonStep @("training/audit_dataset_splits.py", "--root", $root, "--output", (Join-Path $reports "$ExperimentId-split-audit.json"))
Invoke-PythonStep @("training/create_experiment_manifest.py", "--data", $dataYaml, "--experiment-id", "$ExperimentId-before-training", "--output", (Join-Path $reports "$ExperimentId-before-training-manifest.json"))
Invoke-PythonStep @(
    "training/train_detector.py",
    "--model", $checkpoint,
    "--data", $dataYaml,
    "--epochs", "$Epochs",
    "--imgsz", "$ImageSize",
    "--batch", "1",
    "--device", $Device,
    "--workers", "0",
    "--project", "runs/coconut",
    "--name", $runName
)
if (-not (Test-Path -LiteralPath $bestWeights -PathType Leaf)) {
    throw "Training ended without the expected best checkpoint: $bestWeights"
}
Invoke-PythonStep @(
    "training/evaluate_detector.py",
    "--weights", $bestWeights,
    "--data", $dataYaml,
    "--imgsz", "$ImageSize",
    "--batch", "1",
    "--device", $Device,
    "--output", $testReport
)
Invoke-PythonStep @(
    "training/create_experiment_manifest.py",
    "--data", $dataYaml,
    "--weights", $bestWeights,
    "--experiment-id", $ExperimentId,
    "--notes", "Local baseline run; inspect all settings and deviations before publication.",
    "--output", $manifest
)
Invoke-PythonStep @(
    "training/audit_experiment_report.py",
    "--manifest", $manifest,
    "--report", $testReport,
    "--output", $audit
)

Write-Host ([Environment]::NewLine + "Baseline pipeline completed. Review these local files:") -ForegroundColor Green
Write-Host "Test metrics: $testReport"
Write-Host "Provenance audit: $audit"
Write-Host "Split audit: $(Join-Path $reports "$ExperimentId-split-audit.json")"
Write-Host "Do not publish metrics until you inspect the test images, labels, split audit, and provenance audit."

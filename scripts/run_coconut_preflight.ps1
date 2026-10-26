# Run the Coconut dataset preflight from any current directory.
# Read-only with respect to annotation/rights/review inputs. Writes only the JSON report.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$Image0032
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$Preflight = Join-Path $RepoRoot "tools/run_coconut_dataset_preflight.py"
$Annotations = Join-Path $RepoRoot "data/review_batch_2026-10-22/ai_annotation_draft_NOT_FOR_TRAINING.json"
$RightsCsv = Join-Path $RepoRoot "data/review_batch_2026-10-18/source_rights_audit_2026-10-19.csv"
$ReviewCsv = Join-Path $RepoRoot "data/review_batch_2026-10-18/candidate_review_2026-10-18.csv"
$Report = Join-Path $RepoRoot "reports/coconut-preflight-report.json"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python was not found on PATH. Install/use an existing Python environment, then rerun this script. No packages are installed automatically."
}

foreach ($Path in @($Preflight, $Annotations, $RightsCsv, $ReviewCsv)) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Required project file was not found: $Path. Confirm you are running this script from a complete Coconut-Harvest-AI checkout."
    }
}

$Arguments = @(
    $Preflight,
    "--annotations", $Annotations,
    "--rights-csv", $RightsCsv,
    "--review-csv", $ReviewCsv,
    "--output", $Report
)

if ($Image0032) {
    if (-not (Test-Path -LiteralPath $Image0032 -PathType Leaf)) {
        throw "The supplied candidate 0032 image was not found: $Image0032"
    }
    $Draft0032 = $Annotations
    $Arguments += @("--candidate-0032-annotations", $Draft0032, "--image-0032", (Resolve-Path -LiteralPath $Image0032).Path)
}

Push-Location $RepoRoot
try {
    & python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Coconut dataset preflight exited with code $LASTEXITCODE. Read the error above; do not mark any candidate approved based on a partial run."
    }
}
finally {
    Pop-Location
}

Write-Host ""
Write-Host "Preflight report written to: $Report"
Write-Host "This report does not approve annotations, verify legal rights independently, or authorize training."

@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo.
echo ============================================================
echo  PUI89 Coconut Harvest AI - Local Detector Benchmark
echo ============================================================
echo This launcher uses files already on your computer.
echo It does NOT download model weights or upload images.
echo Latency results are not accuracy results.
echo.

if not exist "apps\pui89_app\benchmark_local_detector.py" (
  echo ERROR: Benchmark module not found.
  echo Please run this file from the root of your Coconut-Harvest-AI clone.
  pause
  exit /b 1
)

where python >nul 2>nul
if errorlevel 1 (
  echo ERROR: Python was not found on PATH.
  echo Install Python 3.10 or newer, then reopen Command Prompt.
  echo You can also try the Windows launcher command: py --version
  pause
  exit /b 1
)

python --version
echo.
echo Checking required Python packages without installing anything...
python -c "import torch, PIL, ultralytics"
if errorlevel 1 (
  echo.
  echo ERROR: One or more required packages are missing or cannot import.
  echo No packages were installed by this launcher.
  echo Review the repository setup instructions before installing dependencies.
  pause
  exit /b 1
)

echo.
set /p MODEL_PATH=Enter full path to an existing trusted coconut-trained .pt model:
if not defined MODEL_PATH (
  echo ERROR: Model path is required.
  pause
  exit /b 1
)
if not exist "%MODEL_PATH%" (
  echo ERROR: The model file does not exist at that path.
  pause
  exit /b 1
)

echo.
set /p IMAGE_PATH=Enter full path to one permitted local test image:
if not defined IMAGE_PATH (
  echo ERROR: Image path is required.
  pause
  exit /b 1
)
if not exist "%IMAGE_PATH%" (
  echo ERROR: The image file does not exist at that path.
  pause
  exit /b 1
)

echo.
echo Running a CPU/GPU auto-detected latency benchmark...
echo Report will be written to coconut_latency_benchmark.json in this folder.
python -m apps.pui89_app.benchmark_local_detector --model "%MODEL_PATH%" --image "%IMAGE_PATH%" --device auto --output "coconut_latency_benchmark.json"
if errorlevel 1 (
  echo.
  echo Benchmark failed. Review the error above; no result is claimed.
  pause
  exit /b 1
)

echo.
echo Benchmark completed. This report measures single-image latency only.
echo It does not prove precision, recall, mAP, orchard generalisation, or robot safety.
echo Do not publish model performance claims until you run a reviewed held-out dataset.
pause
endlocal

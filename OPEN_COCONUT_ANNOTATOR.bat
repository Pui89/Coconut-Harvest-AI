@echo off
setlocal
cd /d "%~dp0"

if not exist "tools\coconut_annotator.html" (
  echo ERROR: tools\coconut_annotator.html was not found.
  echo Run this file from the downloaded Coconut-Harvest-AI repository.
  pause
  exit /b 1
)

echo Opening the offline coconut image annotator in your default browser.
echo Choose image files stored on your computer; the tool does not upload them.
start "" "%CD%\tools\coconut_annotator.html"
endlocal

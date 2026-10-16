@echo off
setlocal
cd /d "%~dp0"

echo.
echo Coconut Harvest AI - Free Local Agent
echo This script does not install packages or download models.
echo.

where py >nul 2>nul
if %errorlevel%==0 (
    set "PYTHON=py -3"
) else (
    set "PYTHON=python"
)

%PYTHON% scripts\check_local_agent_environment.py
if errorlevel 1 (
    echo.
    echo Read the message above. No packages were installed.
    pause
    exit /b 1
)

echo.
echo Running the local rule-based agent...
%PYTHON% agents\harvest_planning_agent.py
echo.
echo Finished. This was a synthetic demonstration, not a real camera test.
pause

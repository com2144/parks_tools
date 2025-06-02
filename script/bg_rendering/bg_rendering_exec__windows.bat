@echo off
setlocal enabledelayedexpansion

:: The parent of the parent directory
set "SCRIPT_DIR=%~dp0"
for %%A in ("%SCRIPT_DIR%..\..") do set "PARENT_DIR=%%~fA"


:: Define the JSON file path
set "JSON_PATH=%PARENT_DIR%\hou_env_dir.json"


:: Check if the JSON file exists using PowerShell
powershell -NoProfile -Command ^
    "if (-Not (Test-Path '%JSON_PATH%')) { exit 1 }"

IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] JSON file is not Exists.
    echo Execution "setup_env.exe" !
    pause
    exit /b 1
)


:: Parse the JSON file using PowerShell and extract 'hou_dir'
for /f "delims=" %%A in ('powershell -NoProfile -Command ^
    "$json = Get-Content -Raw -Path \"%JSON_PATH%\" | ConvertFrom-Json; $json.hou_dir"') do (
    set "HOU_DIR=%%A"
)


:: Set the path to 'hython'
set "HOU_HYTHON=%HOU_DIR%\bin\hython.exe"

:: Execute the Python script with 'hython'
"%HOU_HYTHON%" "%SCRIPT_DIR%\bg_rendering.py"


:: If error occurs, pause (to keep the window open)
IF %ERRORLEVEL% NEQ 0 (
    pause
)

endlocal
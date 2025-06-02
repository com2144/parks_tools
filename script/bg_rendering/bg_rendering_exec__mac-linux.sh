#!/bin/bash


# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


# Get the parent of the parent directory
PARENT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"


# Define the JSON file path
JSON_PATH="$PARENT_DIR/hou_env_dir.json"


# Check if the JSON file exists
if [ ! -f "$JSON_PATH" ]; then
    echo "[ERROR] JSON file does not exist: $JSON_PATH"
    echo Execution "setup_env.exe" !
    exit 1
fi


# Parse the JSON file and extract 'hou_dir'
HOU_DIR=$(grep '"hou_dir"' "$JSON_PATH" | sed 's/.*: *"//' | sed 's/".*//')


# Set the path to 'hython'
HOU_HYTHON="$HOU_DIR/bin/hython"

# Execute the Python script with 'hython'
"$HOU_HYTHON" "$SCRIPT_DIR/bg_rendering.py"
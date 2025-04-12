#!/bin/bash
REQUIREMENTS_FILE="dependencies.txt"
HOMEDIR=$(eval echo ~$USER)
WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$HOMEDIR/marauder-uart-gui-python3venv"
DESKTOP_FILE="$HOMEDIR/Desktop/mUg.desktop"
DESKTOP_FILE="$HOMEDIR/Työpöytä/mUg.desktop" #comment this line if you don't have the finnish legends -package.



# Get the user's home directory dynamically
USER_HOME=$(eval echo ~$USER)

# Define the path to the virtual environment
VENV_PATH="$USER_HOME/marauder-uart-gui-python3venv"
REQUIREMENTS_FILE="$WORKDIR/dependencies.txt"

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Install libraries from requirements.txt if it exists
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies from $REQUIREMENTS_FILE..."
    pip3 install -r "$REQUIREMENTS_FILE"
else
    echo "$REQUIREMENTS_FILE not found. Skipping installation."
fi

python $WORKDIR/main.pyw
deactivate

echo "Virtual environment deactivated."

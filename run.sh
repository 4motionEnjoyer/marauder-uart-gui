#!/bin/bash
REQUIREMENTS_FILE="dependencies.txt"
HOMEDIR=$(eval echo ~$USER)
WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$HOMEDIR/marauder-uart-gui-python3venv"
DESKTOP_FILE="$HOMEDIR/Desktop/mUg.desktop"
#DESKTOP_FILE="$HOMEDIR/Työpöytä/mUg.desktop" #comment this line if you don't have the finnish legends -package.


VENV_PATH="$HOMEDIR/marauder-uart-gui-python3venv"

source "$VENV_PATH/bin/activate"
python $WORKDIR/main.pyw
deactivate

echo "Virtual environment deactivated."

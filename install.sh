#!/bin/bash

REQUIREMENTS_FILE="dependencies.txt"
HOMEDIR=$(eval echo ~$USER)
WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$HOMEDIR/marauder-uart-gui-python3venv"
DESKTOP_FILE="$HOMEDIR/Desktop/mUg.desktop"
#DESKTOP_FILE="$HOMEDIR/Työpöytä/mUg.desktop" #comment this line if you don't have the finnish legends -package.

# Check if the virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment not found at $VENV_PATH. Creating a new one..."

    # Create the virtual environment
    python3 -m venv "$VENV_PATH"

    # Check if the virtual environment creation was successful
    if [ $? -eq 0 ]; then
        echo "Virtual environment created successfully at $VENV_PATH"
    else
        echo "Failed to create virtual environment. Exiting."
        exit 1
    fi
else
    echo "Virtual environment already exists at $VENV_PATH"
fi

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Install libraries from requirements.txt if it exists
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies from $REQUIREMENTS_FILE..."
    pip3 install -r "$REQUIREMENTS_FILE"
else
    echo "$REQUIREMENTS_FILE not found. Skipping installation."
fi 

echo "Creating desktop shortcut at $DESKTOP_FILE..."

touch $DESKTOP_FILE
#cat <<EOF > "$DESKTOP_FILE"
echo "[Desktop Entry]
Name=Marauder UART GUI
Comment=Launch the Marauder UART GUI App
Exec=$WORKDIR/run.sh
Icon=$WORKDIR/icon.png
Terminal=true
Type=Application
Categories=Utility;
EOF" > $DESKTOP_FILE

chmod +x "$DESKTOP_FILE"

# Optional: Copy to application menu
cp "$DESKTOP_FILE" "$HOMEDIR/.local/share/applications/"

echo "Desktop shortcut created and installed to application menu."

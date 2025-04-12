#!/bin/bash

# Get the user's home directory dynamically
USER_HOME=$(eval echo ~$USER)

# Define the path to the virtual environment
VENV_PATH="$USER_HOME/marauder-uart-gui-python3venv"
REQUIREMENTS_FILE="dependencies.txt"

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

# If no requirements.txt, manually install dependencies
# (optional, if you want to hardcode a list of libraries instead)
# echo "Installing libraries manually..."
# pip3 install library1 library2 library3

# Run your Python application
python main.py

# Deactivate the virtual environment
deactivate

# Done
echo "Virtual environment deactivated."

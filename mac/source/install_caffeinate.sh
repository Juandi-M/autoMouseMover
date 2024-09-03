#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Check if caffeinate is installed
if ! command_exists caffeinate; then
    echo "caffeinate is not installed. Attempting to install it."

    # Check if Homebrew is installed
    if ! command_exists brew; then
        echo "Homebrew is not installed. Attempting to install Homebrew."
        
        # Check if curl is available
        if command_exists curl; then
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        else
            echo "Error: curl is not installed. Cannot install Homebrew."
            exit 1
        fi

        # Verify Homebrew installation
        if ! command_exists brew; then
            echo "Failed to install Homebrew. Please install it manually."
            exit 1
        fi
    fi

    # Install caffeinate using Homebrew
    brew install caffeinate

    if [ $? -eq 0 ]; then
        echo "caffeinate installed successfully."
    else
        echo "Failed to install caffeinate. Please install it manually."
        exit 1
    fi
else
    echo "caffeinate is already installed."
fi

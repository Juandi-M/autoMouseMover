# 🖱️ Mouse Mover for macOS

![Python](https://img.shields.io/badge/python-v3.11-blue.svg)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-Completed-brightgreen.svg)

## Overview

**Mouse Mover for macOS** is a simple yet powerful application designed to keep your macOS system active by simulating mouse movements. This tool is particularly useful for preventing your computer from going to sleep or activating screensavers during presentations or while performing long-running tasks.

## Tech Stack

- **Python 3.11**: The core language used to develop the application.
- **Tkinter**: Utilized for creating the graphical user interface (GUI).
- **CustomTkinter**: An extension of Tkinter used to create a modern and visually appealing interface.
- **Pillow (PIL)**: Used for handling images, specifically the flags for language switching.
- **pyautogui**: Handles the mouse movement simulation.
- **shutil**: Used to check for the presence of the `caffeinate` tool.
- **subprocess**: Executes shell commands to install missing dependencies and manage processes like `caffeinate`.
- **logging**: Logs the application's activity, useful for tracking and debugging.
- **requests**: Fetches the flag images from the web.

## Features

- **Multilingual Support**: The application supports both English and Spanish. Users can easily switch between languages using intuitive flag buttons.
- **Responsive GUI**: The application interface is responsive and adapts to different screen sizes, with all buttons and labels centrally aligned.
- **Modern UI**: A clean and modern user interface, designed with CustomTkinter for a better visual experience.
- **Mouse Movement Simulation**: Automatically moves the mouse at regular intervals to prevent the system from going idle.
- **Logging**: All actions and events are logged to a file for tracking and debugging purposes.
- **Auto-Installation of Dependencies**: Automatically checks and installs required dependencies, including the `caffeinate` tool on macOS.
- **Custom Icons**: Includes a custom icon set for the application.

## Installation

### Prerequisites

Ensure you have Python 3.11 installed on your macOS system. You can check your Python version by running:

```bash
python3 --version
```

### Clone the Repository

```bash
git clone https://github.com/yourusername/autoMouseMover.git
cd autoMouseMover/mac/source
```

### Install Required Python Packages

Install the required Python libraries using `pip`:

```bash
pip install -r requirements.txt
```

If you don't have `pip` installed, you can install it by following the instructions [here](https://pip.pypa.io/en/stable/installation/).

### Application Icon

The application uses a custom icon set, located in the `mac/source/` directory. The icons are in `.icns` format, specifically designed for macOS applications.

### Package Creation

If you wish to package the application into a standalone executable, you can use `PyInstaller`. The application is already configured with a `.spec` file:

```bash
pyinstaller main.spec
```

This will generate a `dist` folder with the packaged application.

### Shell Script Initialization

The application includes a shell script `install_caffeinate.sh` located in the `mac/source/` directory. This script checks if the `caffeinate` command is installed on the system and installs it via Homebrew if it's missing.

## How It Works

- **Language Switching**: Choose between English and Spanish by clicking the respective flag at the top of the window. The interface will update immediately to reflect your language choice.
  
- **Start and Stop**: Click "Start" to begin simulating mouse movements. The application will log how many times the mouse has moved and display the elapsed time. Click "Stop" to halt the simulation.

- **Auto Installation of `caffeinate`**: If the `caffeinate` command is not found on your system, the application will attempt to install it automatically using Homebrew.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Screenshots

![Screenshot](path/to/screenshot.png)
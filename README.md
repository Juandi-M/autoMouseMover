
# Mouse Mover

## Overview

Mouse Mover is a Python application that moves the mouse cursor at a specified interval to prevent the computer from going to sleep. The application provides a simple GUI for starting and stopping mouse movement, and it also shows a timer and a counter to indicate how long it has been running and how many times the mouse has moved.

## Features

- Moves the mouse cursor up and down at a specified interval.
- Displays the elapsed time and movement counter.
- Provides Start and Stop buttons for controlling mouse movement.
- Includes logging for debugging and tracking.
- Prevents the system from going to sleep while running (Windows and macOS).

## Requirements

- Python 3.x
- Tkinter
- pyautogui
- ctypes (Windows only)

## Installation

1. Clone the repository.
    ```bash
    git clone https://github.com/your-username/mouse-mover.git
    ```

2. Navigate to the directory.
    ```bash
    cd mouse-mover
    ```

3. Install the required packages.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

- For macOS:
    ```bash
    python3 main_mac.py
    ```

- For Windows:
    ```bash
    python main_windows.py
    ```

## Screenshots

(Include some screenshots of the application here)

## License
TBD

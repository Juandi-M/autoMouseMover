# mac/app/config.py
import os

# App Information
APP_NAME = "Mouse Mover for macOS"
MIN_WINDOW_SIZE = (300, 150)

# Mouse Movement Settings
MOVE_INTERVAL = 5  # seconds between moves
MOVE_DISTANCE = 10  # pixels to move
MOVE_DELAY = 0.5  # delay between movements

# Thread Settings
THREAD_TIMEOUT = 1.0

# UI Elements
FLAG_URLS = {
    "us": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/32px-Flag_of_the_United_States.svg.png",
    "spain": "https://upload.wikimedia.org/wikipedia/en/thumb/9/9a/Flag_of_Spain.svg/32px-Flag_of_Spain.svg.png",
}

# File Paths
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LANG_PATH = os.path.join(BASE_PATH, "mac", "app", "lang")
LOG_DIR = os.path.join(BASE_PATH, "logs")
LOG_FILE = os.path.join(LOG_DIR, "mouse_mover.log")
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# Internal Scripts
INTERNAL_DIR = os.path.join(BASE_PATH, "mac", "scripts")
CAFFEINATE_SCRIPT = os.path.join(INTERNAL_DIR, "install_caffeinate.sh")

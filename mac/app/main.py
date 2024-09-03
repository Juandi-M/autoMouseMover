import sys
import os

# Add the directory containing `app` to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from app.gui import MouseMoverApp
from app.utils import init_logger

def main():
    init_logger()
    app = MouseMoverApp()
    app.run()

if __name__ == '__main__':
    main()

# mac/app/main.py
import os
import sys

# Add the project root and mac directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
mac_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
sys.path.insert(0, mac_dir)

import subprocess
import logging
import tkinter.messagebox

# Update imports to use local imports
from app.ui import MouseMoverApp
from app.utils import init_logger
from app.config import CAFFEINATE_SCRIPT, LOG_DIR, LOG_FILE

def ensure_log_directory():
    """Ensure the log directory exists."""
    try:
        # Ensure the full path to the log file exists
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        print(f"Created log directory: {LOG_DIR}")
    except OSError as e:
        print(f"Error creating log directory: {e}")
        sys.exit(1)

def run_install_script():
    """Run the caffeinate installation script."""
    if os.path.exists(CAFFEINATE_SCRIPT):
        try:
            logging.info(f"Running caffeinate script: {CAFFEINATE_SCRIPT}")
            result = subprocess.run(['sh', CAFFEINATE_SCRIPT], 
                                    capture_output=True, 
                                    text=True, 
                                    check=True)
            logging.info("Caffeinate script executed successfully")
            
            # Log any output from the script
            if result.stdout:
                logging.info(f"Caffeinate script output: {result.stdout}")
            if result.stderr:
                logging.warning(f"Caffeinate script warnings: {result.stderr}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running caffeinate script: {e}")
            logging.error(f"Script stdout: {e.stdout}")
            logging.error(f"Script stderr: {e.stderr}")
    else:
        logging.warning(f"Caffeinate script not found at {CAFFEINATE_SCRIPT}")

def main():
    # Ensure log directory exists BEFORE configuring logging
    ensure_log_directory()

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE, mode='w'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    try:
        # Log system and environment information
        logging.info(f"Python version: {sys.version}")
        logging.info(f"Current working directory: {os.getcwd()}")
        logging.info(f"Python path: {sys.path}")
        logging.info(f"Log file: {LOG_FILE}")
        
        # Log application start
        logging.info("Mouse Mover Application Starting")
        
        # Run installation script
        run_install_script()
        
        # Create and run app
        app = MouseMoverApp()
        
        # Log just before running
        logging.info("Attempting to start application main loop")
        app.run()
    
    except Exception as e:
        # Log the full error
        logging.error(f"Unhandled exception in main: {e}", exc_info=True)
        
        # Show error dialog
        try:
            root = tkinter.Tk()
            root.withdraw()  # Hide the main window
            tkinter.messagebox.showerror(
                "Application Error", 
                f"An error occurred:\n{e}\n\nCheck the log file at {LOG_FILE} for details."
            )
        except Exception as dialog_err:
            logging.error(f"Error showing error dialog: {dialog_err}")
        
        # Print to console as a fallback
        print(f"Critical error: {e}")
        sys.exit(1)
    
    finally:
        logging.info("Mouse Mover Application Closed")

if __name__ == '__main__':
    main()
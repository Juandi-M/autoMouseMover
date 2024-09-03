import subprocess
import os

def run_install_script():
    # Get the path to the install_caffeinate.sh script in the _internal directory
    script_path = os.path.join(os.path.dirname(__file__), '_internal', 'install_caffeinate.sh')
    
    # Run the script
    subprocess.call(['sh', script_path])

# Run the installation script first
run_install_script()

# Now proceed with the rest of your application
from app.gui import MouseMoverApp
from app.utils import init_logger

def main():
    init_logger()
    app = MouseMoverApp()
    app.run()

if __name__ == '__main__':
    main()

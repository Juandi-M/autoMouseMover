from gui import MouseMoverApp
from utils import init_logger

def main():
    init_logger()
    app = MouseMoverApp()
    app.run()

if __name__ == '__main__':
    main()

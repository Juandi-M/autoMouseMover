import tkinter as tk
import logging
from .window_setup import setup_main_window
from .thread_handlers import ThreadManager
from app.state_manager import StateManager, AppState
from app.event_handler import AppEventHandler
from app.utils import load_language, update_labels

class MouseMoverApp:
    def __init__(self):
        # Initialize core managers and state
        self.state_manager = StateManager()
        self.thread_manager = ThreadManager(self)
        self.event_handler = AppEventHandler(self)

        # Initialize application state
        self.current_lang = "en"
        self.languages = load_language(self.current_lang)
        self.mouse_move_count = 0
        self.caffeinate_process = None

        # Create main window
        self.root, self.ui_components = setup_main_window(self)

    def start_moving(self):
        """Start mouse movement."""
        self.thread_manager.start_threads()

    def stop_moving(self):
        """Stop mouse movement."""
        self.thread_manager.stop_threads()

    def handle_system_sleep(self):
        """Handle system sleep event."""
        logging.info("System going to sleep")
        if self.state_manager.current_state == AppState.RUNNING:
            self.stop_moving()
        self.state_manager.transition_to(AppState.SLEEPING)

    def handle_system_wake(self):
        """Handle system wake event."""
        logging.info("System waking up")
        self.state_manager.transition_to(AppState.STOPPED)
        update_labels(self)

    def handle_minimize(self):
        """Handle window minimize event."""
        if self.state_manager.current_state not in [AppState.SLEEPING, AppState.SHUTTING_DOWN]:
            self.state_manager.transition_to(AppState.MINIMIZED)
            logging.info("Application minimized")

    def handle_restore(self):
        """Handle window restore event."""
        if self.state_manager.current_state == AppState.MINIMIZED:
            self.state_manager.restore_previous_state()
            logging.info("Application restored")

    def on_closing(self):
        """Handle application closing."""
        logging.info("Application shutting down")
        self.state_manager.transition_to(AppState.SHUTTING_DOWN)
        self.stop_moving()
        self.root.quit()
        self.root.destroy()

    def run(self):
        """Run the application main loop."""
        try:
            self.root.mainloop()
        except Exception as e:
            logging.critical(f"Unhandled exception in run(): {e}", exc_info=True)
            raise
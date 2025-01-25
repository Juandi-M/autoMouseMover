import tkinter as tk
import customtkinter
import logging

from app.state_manager import StateManager, AppState
from app.event_handler import AppEventHandler
from app.utils import load_language, update_labels
from app.thread_manager import MouseMoverThreadManager  # Updated import
from .window_setup import setup_main_window


class MouseMoverApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Initialize core managers and state
        self.state_manager = StateManager()
        self.thread_manager = MouseMoverThreadManager(self)
        self.event_handler = AppEventHandler(self)

        # Initialize application state
        self.current_lang = "en"
        self.languages = load_language(self.current_lang)
        self.mouse_move_count = 0
        self.caffeinate_process = None
        self.move_interval = 5  # Default 5 seconds

        # Configure the application appearance
        self.title("Mouse Mover")
        self.geometry("1100x580")

        # Set system appearance mode for theme detection
        customtkinter.set_appearance_mode("system")  # Changed from "dark"
        customtkinter.set_default_color_theme("blue")

        # Initialize UI variables
        self.text_var = None
        self.counter_var = None
        self.time_var = None
        self.start_button = None
        self.stop_button = None

        # Set up the main window and UI components
        self.root, self.ui_components = setup_main_window(self)
        # Configure window behavior
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def change_move_interval(self, interval_str: str):
        """Change the mouse movement interval."""
        # Convert string to seconds
        if "minute" in interval_str:
            seconds = 60
        else:
            seconds = int(interval_str.split()[0])

        self.move_interval = seconds
        logging.info(f"Changed move interval to {seconds} seconds")

        # If currently running, restart the threads to apply new interval
        if self.state_manager.current_state == AppState.RUNNING:
            self.stop_moving()
            self.start_moving()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """Change the appearance mode of the application."""
        customtkinter.set_appearance_mode(new_appearance_mode.lower())

    def change_scaling_event(self, new_scaling: str):
        """Change the UI scaling of the application."""
        try:
            new_scaling_float = float(new_scaling.replace("%", "")) / 100
            customtkinter.set_widget_scaling(new_scaling_float)
        except ValueError as e:
            logging.error(f"Error changing scaling: {e}")

    def start_moving(self):
        """Start mouse movement."""
        if not self.state_manager.can_transition_to(AppState.RUNNING):
            return
        self.thread_manager.start_threads()
        self.state_manager.transition_to(AppState.RUNNING)
        update_labels(self)

    def stop_moving(self):
        """Stop mouse movement."""
        self.thread_manager.stop_all_threads()
        self.state_manager.transition_to(AppState.STOPPED)
        update_labels(self)

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
        if self.state_manager.current_state not in [
            AppState.SLEEPING,
            AppState.SHUTTING_DOWN,
        ]:
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
        self.quit()

    def run(self):
        """Run the application main loop."""
        try:
            self.mainloop()
        except Exception as e:
            logging.critical(f"Unhandled exception in run(): {e}", exc_info=True)
            raise

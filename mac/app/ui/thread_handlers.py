# app/ui/thread_handlers.py
import time
import logging
import datetime
import pyautogui
import threading

from app.config import MOVE_INTERVAL, MOVE_DISTANCE, MOVE_DELAY
from app.utils import update_labels
from app.state_manager import AppState  # Import AppState directly

class ThreadManager:
    def __init__(self, app):
        self.app = app
        self.threads = {}
        self.stop_flags = {}

    def start_threads(self):
        """Start mouse movement threads."""
        if not self.app.state_manager.can_transition_to(AppState.RUNNING):
            return

        self.app.mouse_move_count = 0
        self.app.state_manager.transition_to(AppState.RUNNING)
        start_perf_counter = time.perf_counter()

        # Create stop flags
        self.stop_flags = {
            'timer': threading.Event(),
            'mouse_mover': threading.Event()
        }

        # Start threads
        self.threads = {
            'timer': threading.Thread(
                target=self._update_time, 
                args=(start_perf_counter, self.stop_flags['timer']),
                daemon=True
            ),
            'mouse_mover': threading.Thread(
                target=self._move_mouse, 
                args=(start_perf_counter, self.stop_flags['mouse_mover']),
                daemon=True
            )
        }

        # Start threads
        for thread in self.threads.values():
            thread.start()

        update_labels(self.app)
        logging.info("Mouse movement started")

    def stop_threads(self):
        """Stop all running threads."""
        # Set stop flags
        for flag in self.stop_flags.values():
            flag.set()

        # Wait for threads to complete
        for thread in self.threads.values():
            thread.join(timeout=2)

        # Reset threads and flags
        self.threads.clear()
        self.stop_flags.clear()

        # Update application state and labels
        self.app.state_manager.transition_to(AppState.STOPPED)
        update_labels(self.app)
        logging.info("Mouse movement stopped")

    def _update_time(self, start_perf_counter, stop_flag):
        """Update time display thread."""
        while not stop_flag.is_set():
            elapsed_time = time.perf_counter() - start_perf_counter
            self.app.root.after(
                0, 
                self.app.time_var.set, 
                f"{self.app.languages['running_for']} {datetime.timedelta(seconds=int(elapsed_time))}"
            )
            stop_flag.wait(timeout=1.0)

    def _move_mouse(self, start_perf_counter, stop_flag):
        """Mouse movement thread."""
        next_move_time = MOVE_INTERVAL
        while not stop_flag.is_set():
            elapsed_time = time.perf_counter() - start_perf_counter
            if elapsed_time >= next_move_time:
                pyautogui.moveRel(0, MOVE_DISTANCE)
                time.sleep(MOVE_DELAY)
                pyautogui.moveRel(0, -MOVE_DISTANCE)
                self.app.mouse_move_count += 1
                self.app.root.after(
                    0, 
                    self.app.counter_var.set, 
                    f"{self.app.languages['mouse_moved']} {self.app.mouse_move_count} {self.app.languages['times']}"
                )
                next_move_time += MOVE_INTERVAL
            
            stop_flag.wait(timeout=0.1)
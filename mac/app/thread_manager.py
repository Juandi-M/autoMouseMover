import threading
import logging
import time
import datetime
import pyautogui
from typing import Dict, Optional

from app.config import MOVE_INTERVAL, MOVE_DISTANCE, MOVE_DELAY
from app.utils import update_labels
from app.state_manager import AppState


class BaseThreadManager:
    """Base thread management class with generic thread handling capabilities."""
    
    def __init__(self):
        self.threads: Dict[str, threading.Thread] = {}
        self.lock = threading.Lock()
        self.stop_flags: Dict[str, threading.Event] = {}
        
    def add_thread(self, name: str, target, args=()) -> threading.Event:
        """Create and store a new thread with a stop flag."""
        with self.lock:
            # Clean up existing thread if it exists
            if name in self.threads:
                self.stop_thread(name)
            
            stop_flag = threading.Event()
            self.stop_flags[name] = stop_flag
            
            thread = threading.Thread(
                target=target,
                args=args + (stop_flag,),
                name=name,
                daemon=True
            )
            self.threads[name] = thread
            thread.start()
            logging.info(f"Started thread: {name}")
            return stop_flag
    
    def stop_thread(self, name: str, timeout: float = 2.0) -> bool:
        """Stop a specific thread."""
        with self.lock:
            if name not in self.threads:
                return True
                
            if name in self.stop_flags:
                self.stop_flags[name].set()
                
            thread = self.threads[name]
            if thread.is_alive():
                thread.join(timeout=timeout)
                success = not thread.is_alive()
                if success:
                    del self.threads[name]
                    if name in self.stop_flags:
                        del self.stop_flags[name]
                    logging.info(f"Stopped thread: {name}")
                else:
                    logging.error(f"Failed to stop thread: {name}")
                return success
            return True
    
    def stop_all_threads(self, timeout: float = 2.0) -> bool:
        """Stop all running threads."""
        success = True
        thread_names = list(self.threads.keys())
        for name in thread_names:
            if not self.stop_thread(name, timeout):
                success = False
        return success


class MouseMoverThreadManager(BaseThreadManager):
    """Specific thread manager for the Mouse Mover application."""
    
    def __init__(self, app):
        super().__init__()
        self.app = app
        self._should_run = threading.Event()

    def start_threads(self):
        """Start mouse movement threads."""
        if not self.app.state_manager.can_transition_to(AppState.RUNNING):
            return

        self._should_run.set()
        self.app.mouse_move_count = 0
        self.app.state_manager.transition_to(AppState.RUNNING)
        start_perf_counter = time.perf_counter()

        # Add timer thread
        self.add_thread(
            'timer', 
            self._update_time, 
            (start_perf_counter,)
        )

        # Add mouse mover thread
        self.add_thread(
            'mouse_mover', 
            self._move_mouse, 
            (start_perf_counter,)
        )

        update_labels(self.app)
        logging.info("Mouse movement started")

    def stop_threads(self):
        """Stop all running threads."""
        self._should_run.clear()  # Signal threads to stop
        success = self.stop_all_threads(timeout=2.0)
        
        if success:
            # Update application state and labels
            self.app.state_manager.transition_to(AppState.STOPPED)
            update_labels(self.app)
            logging.info("Mouse movement stopped")
        else:
            logging.error("Failed to stop all threads")

    def _update_time(self, start_perf_counter, stop_flag):
        """Update time display thread."""
        try:
            while not stop_flag.is_set() and self._should_run.is_set():
                elapsed_time = time.perf_counter() - start_perf_counter
                if self.app and hasattr(self.app, 'time_var'):
                    self.app.time_var.set(
                        f"{self.app.languages['running_for']} {datetime.timedelta(seconds=int(elapsed_time))}"
                    )
                # Check stop condition more frequently
                time.sleep(0.1)
        except Exception as e:
            logging.error(f"Error in time update thread: {e}")

    def _move_mouse(self, start_perf_counter, stop_flag):
            """Mouse movement thread."""
            try:
                next_move_time = time.perf_counter() + self.app.move_interval
                
                while not stop_flag.is_set() and self._should_run.is_set():
                    current_time = time.perf_counter()
                    
                    if current_time >= next_move_time:
                        pyautogui.moveRel(0, MOVE_DISTANCE)
                        time.sleep(MOVE_DELAY)
                        pyautogui.moveRel(0, -MOVE_DISTANCE)
                        
                        if self.app and hasattr(self.app, 'mouse_move_count'):
                            self.app.mouse_move_count += 1
                            self.app.counter_var.set(
                                f"{self.app.languages['mouse_moved']} {self.app.mouse_move_count} {self.app.languages['times']}"
                            )
                        next_move_time = current_time + self.app.move_interval
                    
                    # Check stop condition more frequently
                    time.sleep(0.1)
            except Exception as e:
                logging.error(f"Error in mouse movement thread: {e}")
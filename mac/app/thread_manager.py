# thread_manager.py
import threading
import logging
import time
from typing import Dict, Optional

class ThreadManager:
    def __init__(self):
        self.threads: Dict[str, threading.Thread] = {}
        self.lock = threading.Lock()
        self.stop_flags: Dict[str, threading.Event] = {}
        
    def add_thread(self, name: str, target, args=()) -> threading.Event:
        """Create and store a new thread with a stop flag."""
        with self.lock:
            if name in self.threads and self.threads[name].is_alive():
                logging.warning(f"Thread {name} already exists and running")
                return self.stop_flags[name]
            
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
            
    def stop_thread(self, name: str, timeout: float = 1.0) -> bool:
        """Stop a specific thread."""
        with self.lock:
            if name not in self.threads:
                logging.warning(f"Thread {name} not found")
                return True
                
            if name in self.stop_flags:
                self.stop_flags[name].set()
                
            thread = self.threads[name]
            if thread.is_alive():
                thread.join(timeout=timeout)
                success = not thread.is_alive()
                if success:
                    logging.info(f"Stopped thread: {name}")
                else:
                    logging.error(f"Failed to stop thread: {name}")
                return success
            return True
            
    def stop_all_threads(self, timeout: float = 1.0) -> bool:
        """Stop all running threads."""
        success = True
        with self.lock:
            for name in list(self.threads.keys()):
                if not self.stop_thread(name, timeout):
                    success = False
        return success
        
    def is_thread_running(self, name: str) -> bool:
        """Check if a specific thread is running."""
        with self.lock:
            return name in self.threads and self.threads[name].is_alive()
            
    def cleanup_finished_threads(self):
        """Remove finished threads from tracking."""
        with self.lock:
            for name in list(self.threads.keys()):
                if not self.threads[name].is_alive():
                    del self.threads[name]
                    if name in self.stop_flags:
                        del self.stop_flags[name]
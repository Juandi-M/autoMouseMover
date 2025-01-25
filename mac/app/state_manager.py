# state_manager.py
from enum import Enum
import logging


class AppState(Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    MINIMIZED = "minimized"
    SLEEPING = "sleeping"
    SHUTTING_DOWN = "shutting_down"


class StateManager:
    def __init__(self):
        self.current_state = AppState.STOPPED
        self._previous_state = None

    def transition_to(self, new_state: AppState):
        logging.info(f"State transition: {self.current_state} -> {new_state}")
        self._previous_state = self.current_state
        self.current_state = new_state

    def can_transition_to(self, new_state: AppState) -> bool:
        # Define valid state transitions
        valid_transitions = {
            AppState.STOPPED: [
                AppState.RUNNING,
                AppState.MINIMIZED,
                AppState.SHUTTING_DOWN,
            ],
            AppState.RUNNING: [
                AppState.STOPPED,
                AppState.MINIMIZED,
                AppState.SLEEPING,
                AppState.SHUTTING_DOWN,
            ],
            AppState.MINIMIZED: [
                AppState.RUNNING,
                AppState.STOPPED,
                AppState.SLEEPING,
                AppState.SHUTTING_DOWN,
            ],
            AppState.SLEEPING: [AppState.STOPPED, AppState.RUNNING],
            AppState.SHUTTING_DOWN: [],
        }
        return new_state in valid_transitions.get(self.current_state, [])

    def restore_previous_state(self):
        if self._previous_state:
            self.transition_to(self._previous_state)

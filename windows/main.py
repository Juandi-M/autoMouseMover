import tkinter as tk
from tkinter import ttk
import threading
import time
import datetime
import pyautogui
import logging
import ctypes  # For preventing Windows from going to sleep

# Initialize logging for debugging and tracking
def init_logger():
    logging.basicConfig(
        filename='mouse_mover.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# Function to update elapsed time
def update_time(start_perf_counter, time_var, stop_event):
    while not stop_event.is_set():
        elapsed_time = time.perf_counter() - start_perf_counter
        time_var.set(f"Running for {datetime.timedelta(seconds=int(elapsed_time))}")
        time.sleep(1)

# Function to move the mouse
def move_mouse(stop_event, text_var, counter_var):
    counter = 0
    start_perf_counter = time.perf_counter()
    next_move_time = 6  # Initial offset for mouse movement
    while not stop_event.is_set():
        elapsed_time = time.perf_counter() - start_perf_counter
        if elapsed_time >= next_move_time:
            try:
                pyautogui.moveRel(0, 10)
                time.sleep(0.5)
                pyautogui.moveRel(0, -10)
                counter += 1
                counter_var.set(f"Mouse has moved {counter} times")
                text_var.set("Mouse moving")
                logging.info("Mouse moved successfully.")
                next_move_time += 6  # Schedule the next move
            except pyautogui.FailSafeException:
                logging.warning("FailSafeException triggered, moving mouse to center.")
                text_var.set("FailSafeException, moved to center")
                stop_event.set()
        time.sleep(0.1)  # Sleep for a short while before checking again

# Main function for GUI
def main():
    init_logger()

    # Prevent Windows from going to sleep
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001
    ctypes.windll.kernel32.SetThreadExecutionState(
        ES_CONTINUOUS | ES_SYSTEM_REQUIRED)

    # Tkinter GUI setup
    root = tk.Tk()
    root.title("Mouse Mover for Windows")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    text_var = tk.StringVar()
    text_var.set("Press Start to move mouse")
    label = ttk.Label(frame, textvariable=text_var)
    label.grid(row=0, column=0, columnspan=2)

    counter_var = tk.StringVar()
    counter_var.set("Mouse has not moved yet")
    counter_label = ttk.Label(frame, textvariable=counter_var)
    counter_label.grid(row=1, column=0, columnspan=2)

    time_var = tk.StringVar()
    time_var.set("Not started yet")
    time_label = ttk.Label(frame, textvariable=time_var)
    time_label.grid(row=2, column=0, columnspan=2)

    stop_event = threading.Event()

    def start_moving():
        stop_event.clear()
        start_perf_counter = time.perf_counter()
        threading.Thread(target=update_time, args=(start_perf_counter, time_var, stop_event)).start()
        threading.Thread(target=move_mouse, args=(stop_event, text_var, counter_var)).start()

    def stop_moving():
        stop_event.set()
        text_var.set("Mouse stopped")
        counter_var.set("Mouse has not moved yet")

    start_button = ttk.Button(frame, text="Start", command=start_moving)
    start_button.grid(row=3, column=0)

    stop_button = ttk.Button(frame, text="Stop", command=stop_moving)
    stop_button.grid(row=3, column=1)

    root.mainloop()

if __name__ == '__main__':
    main()
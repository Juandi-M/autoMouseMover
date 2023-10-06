import tkinter as tk
from tkinter import ttk
import threading
import time
import pyautogui
import logging
import ctypes  # Used to prevent system sleep on Windows
import datetime

# Initialize logging
def init_logger():
    logging.basicConfig(
        filename='mouse_mover.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# Function to prevent Windows from going to sleep
def prevent_sleep():
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001
    ctypes.windll.kernel32.SetThreadExecutionState(
        ES_CONTINUOUS | ES_SYSTEM_REQUIRED)

# Move mouse function
def move_mouse(stop_event, text_var, counter_var):
    counter = 0  # Reset counter when this function is called
    while not stop_event.is_set():
        try:
            pyautogui.moveRel(0, 10)  # move mouse 10 pixels down
            time.sleep(0.01)
            pyautogui.moveRel(0, -10)  # move mouse 10 pixels up
            counter += 1
            counter_var.set(f"Mouse has moved {counter} times")
            text_var.set("Mouse moving")
            logging.info("Mouse moved successfully.")
            time.sleep(59)
        except pyautogui.FailSafeException:
            logging.warning("FailSafeException triggered, moving mouse to center.")
            text_var.set("FailSafeException, moved to center")
            stop_event.set()

# Main function for GUI
def main():
    init_logger()
    prevent_sleep()

    # Tkinter GUI setup
    root = tk.Tk()
    root.title("Mouse Mover")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    text_var = tk.StringVar()
    text_var.set("Press Start to move mouse")

    counter_var = tk.StringVar()
    counter_var.set("Mouse has not moved yet")

    label = ttk.Label(frame, textvariable=text_var)
    label.grid(row=0, column=0, columnspan=2)

    counter_label = ttk.Label(frame, textvariable=counter_var)
    counter_label.grid(row=1, column=0, columnspan=2)

    stop_event = threading.Event()

    def start_moving():
        stop_event.clear()
        t = threading.Thread(target=move_mouse, args=(stop_event, text_var, counter_var))
        t.start()
        logging.info("Mouse movement started.")

    def stop_moving():
        stop_event.set()
        text_var.set("Mouse stopped")
        counter_var.set("Mouse has not moved yet")  # Resetting the counter display
        logging.info("User stopped the mouse movement.")

    start_button = ttk.Button(frame, text="Start", command=start_moving)
    start_button.grid(row=2, column=0)

    stop_button = ttk.Button(frame, text="Stop", command=stop_moving)
    stop_button.grid(row=2, column=1)

    root.mainloop()

if __name__ == '__main__':
    main()

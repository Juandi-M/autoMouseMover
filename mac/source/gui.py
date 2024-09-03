import tkinter as tk
from tkinter import ttk
from utils import load_language, switch_language, update_labels, load_flag_image
import time
import threading
import datetime
import pyautogui
import sys

class MouseMoverApp:
    def __init__(self):
        self.current_lang = "en"
        # Update the load_language call to reference the correct path
        self.languages = load_language(self.current_lang)
        self.mouse_move_count = 0
        self.stop_event = threading.Event()
        self.caffeinate_process = None

        self.root = tk.Tk()
        self.setup_gui()


    def setup_gui(self):
        self.root.title("Mouse Mover for macOS")
        self.root.minsize(300, 150)

        # Main frame setup
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Language buttons frame
        lang_frame = ttk.Frame(self.root, padding="5")
        lang_frame.grid(row=0, column=0, pady=10, sticky="ew")

        self.root.columnconfigure(0, weight=1)
        lang_frame.columnconfigure(0, weight=1)
        lang_frame.columnconfigure(1, weight=1)

        # Add flag buttons
        self.add_flag_buttons(lang_frame)

        # Add labels and buttons
        self.add_labels_and_buttons(main_frame)

    def add_flag_buttons(self, lang_frame):
        us_flag_url = "https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/32px-Flag_of_the_United_States.svg.png"
        spain_flag_url = "https://upload.wikimedia.org/wikipedia/en/thumb/9/9a/Flag_of_Spain.svg/32px-Flag_of_Spain.svg.png"

        self.us_flag = load_flag_image(us_flag_url)
        self.spain_flag = load_flag_image(spain_flag_url)

        us_button = tk.Button(
            lang_frame, image=self.us_flag, command=lambda: switch_language("en", self), 
            relief="flat", bd=0, cursor="hand2", highlightthickness=0, 
            bg=self.root['bg'], activebackground=self.root['bg']
        )
        us_button.grid(row=0, column=0, padx=5, pady=5)

        spain_button = tk.Button(
            lang_frame, image=self.spain_flag, command=lambda: switch_language("es", self), 
            relief="flat", bd=0, cursor="hand2", highlightthickness=0, 
            bg=self.root['bg'], activebackground=self.root['bg']
        )
        spain_button.grid(row=0, column=1, padx=5, pady=5)

    def add_labels_and_buttons(self, main_frame):
        self.text_var = tk.StringVar()
        self.text_var.set(self.languages["press_start"])
        label = ttk.Label(main_frame, textvariable=self.text_var, anchor="center")
        label.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        self.counter_var = tk.StringVar()
        self.counter_var.set(self.languages["mouse_not_moved"])
        counter_label = ttk.Label(main_frame, textvariable=self.counter_var, anchor="center")
        counter_label.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

        self.time_var = tk.StringVar()
        self.time_var.set(self.languages["not_started_yet"])
        time_label = ttk.Label(main_frame, textvariable=self.time_var, anchor="center")
        time_label.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        self.start_button = ttk.Button(main_frame, text=self.languages["start"], command=self.start_moving)
        self.start_button.grid(row=3, column=0, padx=5, pady=10, sticky="ew")

        self.stop_button = ttk.Button(main_frame, text=self.languages["stop"], command=self.stop_moving)
        self.stop_button.grid(row=3, column=1, padx=5, pady=10, sticky="ew")

    def start_moving(self):
        self.mouse_move_count = 0
        self.stop_event.clear()
        start_perf_counter = time.perf_counter()
        threading.Thread(target=self.update_time, args=(start_perf_counter,)).start()
        threading.Thread(target=self.move_mouse, args=(start_perf_counter,)).start()
        update_labels(self)

    def stop_moving(self):
        self.stop_event.set()
        update_labels(self)
        if self.caffeinate_process:
            self.caffeinate_process.terminate()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        self.stop_moving()
        self.root.destroy()
        sys.exit(0)

    def update_time(self, start_perf_counter):
        while not self.stop_event.is_set():
            elapsed_time = time.perf_counter() - start_perf_counter
            self.root.after(0, self.time_var.set, f"{self.languages['running_for']} {datetime.timedelta(seconds=int(elapsed_time))}")
            time.sleep(1)

    def move_mouse(self, start_perf_counter):
        next_move_time = 5
        while not self.stop_event.is_set():
            elapsed_time = time.perf_counter() - start_perf_counter
            if elapsed_time >= next_move_time:
                pyautogui.moveRel(0, 10)
                time.sleep(0.5)
                pyautogui.moveRel(0, -10)
                self.mouse_move_count += 1
                self.root.after(0, self.counter_var.set, f"{self.languages['mouse_moved']} {self.mouse_move_count} {self.languages['times']}")
                next_move_time += 5
            time.sleep(0.1)
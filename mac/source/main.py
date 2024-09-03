import subprocess
import shutil
import tkinter as tk
from tkinter import ttk
import threading
import time
import datetime
import pyautogui
import logging
import platform
from io import BytesIO
from PIL import Image, ImageTk
import requests
import sys
import os
import importlib.util

# Function to load the appropriate language file
def load_language(lang_code):
    # Ajusta el path usando el absolute path
    lang_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lang_' + lang_code + '.py'))

    # Imprimir la ruta completa para depuración
    print(f"Cargando archivo de idioma desde: {lang_path}")
    
    if not os.path.exists(lang_path):
        raise FileNotFoundError(f"No se encontró el archivo de idioma: {lang_path}")

    spec = importlib.util.spec_from_file_location(f'lang_{lang_code}', lang_path)
    lang_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lang_module)
    
    return lang_module.languages

# Default language is English
current_lang = "en"
languages = load_language(current_lang)
mouse_move_count = 0  # Variable to track how many times the mouse has moved

# Initialize logging
def init_logger():
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'mouse_mover.log')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# Function to switch language
def switch_language(lang):
    global current_lang, languages
    current_lang = lang
    languages = load_language(current_lang)
    update_labels()  # Call the update function to refresh labels

# Initialize logging
def init_logger():
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'mouse_mover.log')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


# Function to switch language
def switch_language(lang):
    global current_lang, languages
    current_lang = lang
    languages = load_language(current_lang)
    update_labels()  # Call the update function to refresh labels

# Function to update all text labels according to the selected language
def update_labels():
    start_button.config(text=languages["start"])
    stop_button.config(text=languages["stop"])
    
    # Update the labels according to the current application state
    if stop_event.is_set():
        text_var.set(languages["mouse_stopped"])
        counter_var.set(languages["mouse_not_moved"])
        time_var.set(languages["not_started_yet"])
    else:
        if mouse_move_count == 0:
            counter_var.set(languages["mouse_not_moved"])
            text_var.set(languages["press_start"])
        else:
            counter_var.set(f"{languages['mouse_moved']} {mouse_move_count} {languages['times']}")
            text_var.set(languages["log_mouse_moved"])

    # Force immediate GUI update
    root.update_idletasks()

# Function to load flag images from the web
def load_flag_image(url):
    response = requests.get(url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    return ImageTk.PhotoImage(img)

# Global stop_event so it can be accessed across functions
stop_event = threading.Event()

# Main function for GUI
def main():
    init_logger()

    global root, text_var, counter_var, time_var, start_button, stop_button

    # Tkinter GUI setup
    root = tk.Tk()
    root.title("Mouse Mover for macOS")

    # Set minimum size for the window
    root.minsize(300, 150)

    # Styling
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 12), padding=6)
    style.configure('TLabel', font=('Arial', 12))

    # Create frame
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Expandable rows and columns
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)

    # Language buttons frame
    lang_frame = ttk.Frame(root, padding="5")
    lang_frame.grid(row=0, column=0, pady=10, sticky="ew")

    # Center language buttons frame
    root.columnconfigure(0, weight=1)
    lang_frame.columnconfigure(0, weight=1)
    lang_frame.columnconfigure(1, weight=1)

    # Load flag images from the web
    us_flag_url = "https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/32px-Flag_of_the_United_States.svg.png"
    spain_flag_url = "https://upload.wikimedia.org/wikipedia/en/thumb/9/9a/Flag_of_Spain.svg/32px-Flag_of_Spain.svg.png"

    us_flag = load_flag_image(us_flag_url)
    spain_flag = load_flag_image(spain_flag_url)

    # Configuration of the flag buttons
    def reset_button_state(button):
        button.config(relief="flat", state="normal")

    def on_click_us():
        switch_language("en")
        root.after(100, lambda: reset_button_state(us_button))

    def on_click_spain():
        switch_language("es")
        root.after(100, lambda: reset_button_state(spain_button))

    us_button = tk.Button(
        lang_frame, image=us_flag, command=on_click_us, relief="flat", 
        bd=0, cursor="hand2", highlightthickness=0, bg=root['bg'], activebackground=root['bg']
    )
    us_button.grid(row=0, column=0, padx=5, pady=5)

    spain_button = tk.Button(
        lang_frame, image=spain_flag, command=on_click_spain, relief="flat", 
        bd=0, cursor="hand2", highlightthickness=0, bg=root['bg'], activebackground=root['bg']
    )
    spain_button.grid(row=0, column=1, padx=5, pady=5)

    # Button hover effect with a simple zoom
    def on_enter(e):
        e.widget.config(width=36, height=36)

    def on_leave(e):
        e.widget.config(width=32, height=32)

    us_button.bind("<Enter>", on_enter)
    us_button.bind("<Leave>", on_leave)

    spain_button.bind("<Enter>", on_enter)
    spain_button.bind("<Leave>", on_leave)

    text_var = tk.StringVar()
    text_var.set(languages["press_start"])
    label = ttk.Label(main_frame, textvariable=text_var, anchor="center")
    label.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

    counter_var = tk.StringVar()
    counter_var.set(languages["mouse_not_moved"])
    counter_label = ttk.Label(main_frame, textvariable=counter_var, anchor="center")
    counter_label.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

    time_var = tk.StringVar()
    time_var.set(languages["not_started_yet"])
    time_label = ttk.Label(main_frame, textvariable=time_var, anchor="center")
    time_label.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

    caffeinate_process = None

    def start_moving():
        global mouse_move_count
        mouse_move_count = 0  # Reset the mouse move count when starting
        stop_event.clear()
        start_perf_counter = time.perf_counter()
        threading.Thread(target=update_time, args=(start_perf_counter, time_var, stop_event)).start()
        threading.Thread(target=move_mouse, args=(stop_event, text_var, counter_var, start_perf_counter)).start()
        update_labels()  # Ensure labels reflect the correct state when starting mouse movement
        if platform.system() == 'Darwin' and is_caffeinate_available():
            try:
                caffeinate_process = subprocess.Popen(['caffeinate'])
                logging.info(languages["caffeinate_started"])
            except Exception as e:
                logging.error(f"{languages['failed_to_start_caffeinate']}: {e}")
        elif platform.system() == 'Darwin':
            logging.warning(languages["caffeinate_not_found"])
            try:
                subprocess.run(["./install_caffeinate.sh"], check=True)  # Call the installation script
            except subprocess.CalledProcessError as e:
                logging.error(f"{languages['failed_install']}: {e}")
                text_var.set(languages["failed_install"])

    def stop_moving():
        stop_event.set()
        update_labels()  # Ensure labels reflect the correct state when stopping mouse movement
        if caffeinate_process:
            caffeinate_process.terminate()
            logging.info(languages["caffeinate_terminated"])

    start_button = ttk.Button(main_frame, text=languages["start"], command=start_moving)
    start_button.grid(row=3, column=0, padx=5, pady=10, sticky="ew")

    stop_button = ttk.Button(main_frame, text=languages["stop"], command=stop_moving)
    stop_button.grid(row=3, column=1, padx=5, pady=10, sticky="ew")

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, stop_moving))  # Handle window close event

    root.mainloop()

# Function to update the elapsed time
def update_time(start_perf_counter, time_var, stop_event):
    while not stop_event.is_set():
        elapsed_time = time.perf_counter() - start_perf_counter
        time_var.set(f"{languages['running_for']} {datetime.timedelta(seconds=int(elapsed_time))}")
        time.sleep(1)

# Function to move the mouse
def move_mouse(stop_event, text_var, counter_var, start_perf_counter):
    global mouse_move_count  # Track mouse movements across functions
    next_move_time = 5  # Move the mouse when this time is reached
    while not stop_event.is_set():
        elapsed_time = time.perf_counter() - start_perf_counter
        if elapsed_time >= next_move_time:
            try:
                pyautogui.moveRel(0, 10)
                time.sleep(0.5)
                pyautogui.moveRel(0, -10)
                mouse_move_count += 1
                counter_var.set(f"{languages['mouse_moved']} {mouse_move_count} {languages['times']}")
                text_var.set(languages["log_mouse_moved"])
                logging.info(languages["log_mouse_moved"])
                next_move_time += 5
            except pyautogui.FailSafeException:
                logging.warning(languages["fail_safe"])
                text_var.set(languages["fail_safe"])
                stop_event.set()
        time.sleep(0.1)  # Sleep for a short while before checking again

# Function to handle the application shutdown gracefully
def on_closing(root, stop_moving):
    stop_moving()
    root.destroy()
    sys.exit(0)  # Ensure all threads are terminated when the window is closed

def is_caffeinate_available():
    """Check if caffeinate command is available"""
    return shutil.which("caffeinate") is not None

if __name__ == '__main__':
    main()

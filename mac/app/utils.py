import sys
import os
import importlib.util
import requests
import logging
from PIL import Image, ImageTk
from io import BytesIO


def load_language(lang_code):
    # Adjust the path to the 'lang' directory within the 'app' directory
    lang_path = os.path.join(os.path.dirname(__file__), 'lang', f'lang_{lang_code}.py')
    print(f"Loading language file from: {lang_path}")
    
    if not os.path.exists(lang_path):
        raise FileNotFoundError(f"Language file not found: {lang_path}")

    spec = importlib.util.spec_from_file_location(f'lang_{lang_code}', lang_path)
    lang_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lang_module)
    
    return lang_module.languages

def init_logger():
    # Adjust the path to the 'logs' directory in the root of the project
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'logs'))
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'mouse_mover.log')
    
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def switch_language(lang, app):
    app.current_lang = lang
    app.languages = load_language(lang)
    update_labels(app)

def update_labels(app):
    app.start_button.config(text=app.languages["start"])
    app.stop_button.config(text=app.languages["stop"])
    
    if app.stop_event.is_set():
        app.text_var.set(app.languages["mouse_stopped"])
        app.counter_var.set(app.languages["mouse_not_moved"])
        app.time_var.set(app.languages["not_started_yet"])
    else:
        if app.mouse_move_count == 0:
            app.counter_var.set(app.languages["mouse_not_moved"])
            app.text_var.set(app.languages["press_start"])
        else:
            app.counter_var.set(f"{app.languages['mouse_moved']} {app.mouse_move_count} {app.languages['times']}")
            app.text_var.set(app.languages["log_mouse_moved"])

    app.root.update_idletasks()

def load_flag_image(url):
    response = requests.get(url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    return ImageTk.PhotoImage(img)


def load_language(lang_code):
    # Adjust the path to the 'lang' directory within the '_internal' directory if bundled
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

    # Path when running the app after bundling with PyInstaller
    lang_path = os.path.join(base_path, '_internal', 'lang', f'lang_{lang_code}.py')

    # Fallback path when running the app from source code
    if not os.path.exists(lang_path):
        lang_path = os.path.join(base_path, 'lang', f'lang_{lang_code}.py')

    print(f"Loading language file from: {lang_path}")

    if not os.path.exists(lang_path):
        raise FileNotFoundError(f"Language file not found: {lang_path}")

    spec = importlib.util.spec_from_file_location(f'lang_{lang_code}', lang_path)
    lang_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lang_module)
    
    return lang_module.languages


def init_logger():
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'mouse_mover.log')
    
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def switch_language(lang, app):
    app.current_lang = lang
    app.languages = load_language(lang)
    update_labels(app)

def update_labels(app):
    app.start_button.config(text=app.languages["start"])
    app.stop_button.config(text=app.languages["stop"])
    
    if app.stop_event.is_set():
        app.text_var.set(app.languages["mouse_stopped"])
        app.counter_var.set(app.languages["mouse_not_moved"])
        app.time_var.set(app.languages["not_started_yet"])
    else:
        if app.mouse_move_count == 0:
            app.counter_var.set(app.languages["mouse_not_moved"])
            app.text_var.set(app.languages["press_start"])
        else:
            app.counter_var.set(f"{app.languages['mouse_moved']} {app.mouse_move_count} {app.languages['times']}")
            app.text_var.set(app.languages["log_mouse_moved"])

    app.root.update_idletasks()

def load_flag_image(url):
    response = requests.get(url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    return ImageTk.PhotoImage(img)

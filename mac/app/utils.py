import sys
import os
import importlib.util
import requests
import logging
from PIL import Image, ImageTk
from io import BytesIO
from app.config import LANG_PATH, LOG_DIR, LOG_FILE, LOG_FORMAT, FLAG_URLS
from app.state_manager import AppState


def init_logger():
    """Initialize the application logger."""
    os.makedirs(LOG_DIR, exist_ok=True)
    
    logging.basicConfig(
        level=logging.DEBUG,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logging.info("Logger initialized")
    logging.info(f"Log file: {LOG_FILE}")


def load_language(lang_code):
    """Load language strings from module."""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    lang_path = os.path.join(base_path, 'lang', f'lang_{lang_code}.py')
    
    if not os.path.exists(lang_path):
        lang_path = os.path.join(LANG_PATH, f'lang_{lang_code}.py')
    
    if not os.path.exists(lang_path):
        raise FileNotFoundError(f"Language file not found: {lang_path}")

    spec = importlib.util.spec_from_file_location(f'lang_{lang_code}', lang_path)
    lang_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lang_module)
    return lang_module.languages


def switch_language(lang, app):
    """Switch the application language."""
    app.current_lang = lang
    app.languages = load_language(lang)
    
    # Update button states if they exist
    if hasattr(app, 'english_btn'):
        app.english_btn.set_active(lang == "en")
    if hasattr(app, 'spanish_btn'):
        app.spanish_btn.set_active(lang == "es")
    
    update_labels(app)


def update_labels(app):
    """Update all UI labels based on application state."""
    # Update button text
    app.start_button.configure(text=app.languages["start"])
    app.stop_button.configure(text=app.languages["stop"])
    
    # Update button states based on app state
    if app.state_manager.current_state == AppState.RUNNING:
        app.start_button.configure(state="disabled")
        app.stop_button.configure(state="normal")
    else:
        app.start_button.configure(state="normal")
        app.stop_button.configure(state="disabled")
    
    # Update status labels based on state
    if app.state_manager.current_state == AppState.STOPPED:
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

    # Ensure UI is updated
    app.update_idletasks()


def load_flag_image(url):
    """Load a flag image from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        return ImageTk.PhotoImage(img)
    except Exception as e:
        logging.error(f"Error loading flag image: {e}")
        return None
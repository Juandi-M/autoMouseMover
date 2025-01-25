import tkinter as tk
import customtkinter
import os
from PIL import Image
from app.config import APP_NAME, MIN_WINDOW_SIZE
from app.utils import load_language, update_labels, switch_language

# Modern dark theme colors
COLORS = {
    "bg": "#1E1E2D",           # Dark background
    "sidebar": "#1A1A27",      # Slightly darker for sidebar
    "button": "#7E6BE8",       # Purple button
    "button_hover": "#6557CC",  # Darker purple for hover
    "stop": "#E11D48",         # Red stop button
    "stop_hover": "#BE123C",   # Darker red for hover
    "text": "#FFFFFF",         # White text
    "text_secondary": "#9CA3AF" # Gray text
}

def setup_main_window(app):
    """Set up the main application window."""
    app.title(APP_NAME)
    app.geometry("800x500")
    
    # Configure the main window
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)
    
    # Force dark mode
    customtkinter.set_appearance_mode("dark")
    
    # Initialize StringVars
    app.text_var = tk.StringVar(value=app.languages["press_start"])
    app.counter_var = tk.StringVar(value=app.languages["mouse_not_moved"])
    app.time_var = tk.StringVar(value=app.languages["not_started_yet"])

    # Create main frames
    navigation_frame = setup_navigation_frame(app)
    main_frame = setup_main_frame(app)

    return app, {
        "navigation_frame": navigation_frame,
        "main_frame": main_frame
    }

def setup_navigation_frame(app):
    """Set up the navigation frame with language switcher and settings."""
    navigation_frame = customtkinter.CTkFrame(
        app,
        fg_color=COLORS["sidebar"],
        corner_radius=15,
        border_width=1,
        border_color="#2A2A3A"
    )
    navigation_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
    navigation_frame.grid_rowconfigure(5, weight=1)
    navigation_frame.configure(width=200)
    navigation_frame.grid_propagate(False)
    navigation_frame.grid_columnconfigure(0, weight=1)

    # Title
    title_frame = customtkinter.CTkFrame(navigation_frame, fg_color="transparent")
    title_frame.grid(row=0, column=0, padx=20, pady=(30, 20), sticky="ew")
    title_frame.grid_columnconfigure(0, weight=1)

    title_label = customtkinter.CTkLabel(
        title_frame,
        text="Mouse Mover",
        font=customtkinter.CTkFont(size=24, weight="bold"),
        text_color=COLORS["text"]
    )
    title_label.grid(row=0, column=0)

    # Language Switcher Section
    lang_frame = customtkinter.CTkFrame(navigation_frame, fg_color="transparent")
    lang_frame.grid(row=1, column=0, sticky="ew", pady=20)
    lang_frame.grid_columnconfigure(0, weight=1)

    lang_label = customtkinter.CTkLabel(
        lang_frame,
        text="Language",
        font=customtkinter.CTkFont(size=14),
        text_color=COLORS["text_secondary"]
    )
    lang_label.grid(row=0, column=0, padx=20, pady=(0, 10), sticky="w")

    # Language Buttons Frame
    lang_buttons = customtkinter.CTkFrame(lang_frame, fg_color="transparent")
    lang_buttons.grid(row=1, column=0, sticky="ew")
    
    # Load flag images
    us_img = customtkinter.CTkImage(
        light_image=Image.open("ui/images/us_flag.png"),
        dark_image=Image.open("ui/images/us_flag.png"),
        size=(24, 24)
    )
    es_img = customtkinter.CTkImage(
        light_image=Image.open("ui/images/es_flag.png"),
        dark_image=Image.open("ui/images/es_flag.png"),
        size=(24, 24)
    )

    # English Button
    app.english_btn = customtkinter.CTkButton(
        lang_buttons,
        text="English",
        image=us_img,
        compound="left",
        command=lambda: switch_language("en", app),
        fg_color=COLORS["button"] if app.current_lang == "en" else "transparent",
        hover_color=COLORS["button_hover"],
    )
    app.english_btn.grid(row=0, column=0, padx=5)

    # Spanish Button
    app.spanish_btn = customtkinter.CTkButton(
        lang_buttons,
        text="Español",
        image=es_img,
        compound="left",
        command=lambda: switch_language("es", app),
        fg_color=COLORS["button"] if app.current_lang == "es" else "transparent",
        hover_color=COLORS["button_hover"],
    )
    app.spanish_btn.grid(row=0, column=1, padx=5)

    # Move Interval Section
    interval_frame = customtkinter.CTkFrame(navigation_frame, fg_color="transparent")
    interval_frame.grid(row=2, column=0, sticky="ew", pady=20)
    interval_frame.grid_columnconfigure(0, weight=1)

    interval_label = customtkinter.CTkLabel(
        interval_frame,
        text="Move Interval",
        font=customtkinter.CTkFont(size=14),
        text_color=COLORS["text_secondary"]
    )
    interval_label.grid(row=0, column=0, padx=20, pady=(0, 10), sticky="w")

    # Move Interval Dropdown
    intervals = ["5 seconds", "10 seconds", "20 seconds", "30 seconds", "1 minute"]
    app.interval_var = customtkinter.StringVar(value=intervals[0])
    interval_dropdown = customtkinter.CTkOptionMenu(
        interval_frame,
        values=intervals,
        variable=app.interval_var,
        command=lambda v: app.change_move_interval(v),
        fg_color=COLORS["button"],
        button_color=COLORS["button_hover"]
    )
    interval_dropdown.grid(row=1, column=0, padx=20, sticky="ew")

    # Font Size Section
    font_frame = customtkinter.CTkFrame(navigation_frame, fg_color="transparent")
    font_frame.grid(row=3, column=0, sticky="ew", pady=20)
    font_frame.grid_columnconfigure(0, weight=1)

    font_label = customtkinter.CTkLabel(
        font_frame,
        text="Font Size",
        font=customtkinter.CTkFont(size=14),
        text_color=COLORS["text_secondary"]
    )
    font_label.grid(row=0, column=0, padx=20, pady=(0, 10), sticky="w")

    # Font Size Dropdown
    font_sizes = ["80%", "90%", "100%", "110%", "120%"]
    app.font_size_var = customtkinter.StringVar(value="100%")
    font_dropdown = customtkinter.CTkOptionMenu(
        font_frame,
        values=font_sizes,
        variable=app.font_size_var,
        command=app.change_scaling_event,
        fg_color=COLORS["button"],
        button_color=COLORS["button_hover"]
    )
    font_dropdown.grid(row=1, column=0, padx=20, sticky="ew")

    return navigation_frame

def setup_main_frame(app):
    """Set up the main content frame."""
    main_frame = customtkinter.CTkFrame(
        app,
        fg_color=COLORS["bg"],
        corner_radius=15,
        border_width=1,
        border_color="#2A2A3A"
    )
    main_frame.grid(row=0, column=1, padx=(0, 15), pady=15, sticky="nsew")

    # Content frame for labels and buttons
    content_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
    content_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)

    # Status labels
    labels_frame = customtkinter.CTkFrame(content_frame, fg_color="transparent")
    labels_frame.grid(row=0, column=0, sticky="nsew")
    labels_frame.grid_columnconfigure(0, weight=1)

    for i, (var, size) in enumerate([
        (app.text_var, 28),
        (app.counter_var, 20),
        (app.time_var, 20)
    ]):
        label = customtkinter.CTkLabel(
            labels_frame,
            textvariable=var,
            font=customtkinter.CTkFont(size=size, weight="bold"),
            text_color=COLORS["text"]
        )
        label.grid(row=i, column=0, pady=10)

    # Buttons
    button_frame = customtkinter.CTkFrame(content_frame, fg_color="transparent")
    button_frame.grid(row=1, column=0, sticky="ew", pady=(20, 0))
    button_frame.grid_columnconfigure((0, 1), weight=1)

    app.start_button = customtkinter.CTkButton(
        button_frame,
        text=app.languages["start"],
        command=app.start_moving,
        font=customtkinter.CTkFont(size=18, weight="bold"),
        fg_color=COLORS["button"],
        hover_color=COLORS["button_hover"],
        height=50,
        corner_radius=12
    )
    app.start_button.grid(row=0, column=0, padx=15, sticky="ew")

    app.stop_button = customtkinter.CTkButton(
        button_frame,
        text=app.languages["stop"],
        command=app.stop_moving,
        font=customtkinter.CTkFont(size=18, weight="bold"),
        fg_color=COLORS["stop"],
        hover_color=COLORS["stop_hover"],
        height=50,
        corner_radius=12,
        state="disabled"
    )
    app.stop_button.grid(row=0, column=1, padx=15, sticky="ew")

    return main_frame
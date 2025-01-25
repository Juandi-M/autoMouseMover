import tkinter as tk
import customtkinter
import os
import logging
from PIL import Image
from app.config import APP_NAME, MIN_WINDOW_SIZE
from app.utils import load_language, update_labels, switch_language

# Theme colors for dark and light modes
COLORS = {
    "dark": {
        "bg": "#1E1E2D",  # Dark background
        "sidebar": "#1A1A27",  # Slightly darker for sidebar
        "button": "#7E6BE8",  # Purple button
        "button_hover": "#6557CC",  # Darker purple for hover
        "stop": "#E11D48",  # Red stop button
        "stop_hover": "#BE123C",  # Darker red for hover
        "text": "#FFFFFF",  # White text
        "text_secondary": "#9CA3AF",  # Gray text
        "border": "#2A2A3A",  # Dark border
    },
    "light": {
        "bg": "#FFFFFF",  # Pure white background
        "sidebar": "#F8FAFC",  # Very light gray for sidebar
        "button": "#7E6BE8",  # Keep purple button
        "button_hover": "#6557CC",  # Darker purple for hover
        "stop": "#E11D48",  # Keep red stop button
        "stop_hover": "#BE123C",  # Darker red for hover
        "text": "#1E293B",  # Dark blue-gray text
        "text_secondary": "#64748B",  # Medium blue-gray text
        "border": "#E2E8F0",  # Light gray border
    },
}


def setup_theme_observer(app):
    """Set up an observer for system theme changes"""
    customtkinter.set_appearance_mode("system")  # Enable system theme

    def update_theme(event=None):
        try:
            colors = get_system_appearance()
            # Update frames first
            if hasattr(app, "navigation_frame") and app.navigation_frame:
                app.navigation_frame.configure(
                    fg_color=colors["sidebar"], border_color=colors["border"]
                )
            if hasattr(app, "main_frame") and app.main_frame:
                app.main_frame.configure(
                    fg_color=colors["bg"], border_color=colors["border"]
                )

            # Update buttons if they exist and are initialized
            if hasattr(app, "start_button") and app.start_button:
                app.start_button.configure(
                    fg_color=colors["button"], hover_color=colors["button_hover"]
                )
            if hasattr(app, "stop_button") and app.stop_button:
                app.stop_button.configure(
                    fg_color=colors["stop"], hover_color=colors["stop_hover"]
                )

            # Update language buttons if they exist
            if hasattr(app, "english_btn") and app.english_btn:
                app.english_btn.configure(
                    fg_color=(
                        colors["button"] if app.current_lang == "en" else "transparent"
                    ),
                    hover_color=colors["button_hover"],
                )
            if hasattr(app, "spanish_btn") and app.spanish_btn:
                app.spanish_btn.configure(
                    fg_color=(
                        colors["button"] if app.current_lang == "es" else "transparent"
                    ),
                    hover_color=colors["button_hover"],
                )

            logging.debug("Theme updated successfully")
        except Exception as e:
            logging.error(f"Error updating theme: {e}")

    app.bind("<<ThemeChanged>>", update_theme)
    return update_theme


def update_language_buttons(app, lang):
    """Update language button appearances"""
    colors = get_system_appearance()
    app.english_btn.configure(
        fg_color=colors["button"] if lang == "en" else "transparent"
    )
    app.spanish_btn.configure(
        fg_color=colors["button"] if lang == "es" else "transparent"
    )


def get_system_appearance():
    """Get the system appearance (dark/light) and return appropriate colors."""
    appearance = customtkinter.get_appearance_mode().lower()
    print(f"Current appearance mode: {appearance}")  # Debug line
    return COLORS[appearance]


def setup_main_window(app):
    # Set appearance mode at startup
    customtkinter.set_appearance_mode("system")
    print(f"Initial appearance mode: {customtkinter.get_appearance_mode()}")

    app.title(APP_NAME)
    app.geometry("800x500")
    app.minsize(600, 400)

    # Configure the main window for responsiveness
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=3)

    # Initialize StringVars
    app.text_var = tk.StringVar(value=app.languages["press_start"])
    app.counter_var = tk.StringVar(value=app.languages["mouse_not_moved"])
    app.time_var = tk.StringVar(value=app.languages["not_started_yet"])
    app.interval_var = tk.StringVar(value="Interval: 5 seconds")

    # Create main frames first
    navigation_frame = setup_navigation_frame(app)
    main_frame = setup_main_frame(app)

    # Store frames as attributes
    app.navigation_frame = navigation_frame
    app.main_frame = main_frame

    # Now initialize theme observer after UI elements are created
    theme_updater = setup_theme_observer(app)

    # Do initial theme update
    theme_updater()

    # Bind window resize event
    app.bind("<Configure>", lambda e: on_window_configure(app, navigation_frame))

    return app, {"navigation_frame": navigation_frame, "main_frame": main_frame}


def on_window_configure(app, nav_frame):
    """Handle window resize events."""
    window_width = app.winfo_width()
    min_nav_width = 180
    max_nav_width = 250

    # Calculate new navigation frame width (20% of window width)
    new_width = min(max(window_width * 0.2, min_nav_width), max_nav_width)
    nav_frame.configure(width=new_width)


def update_interval_text(app, value):
    """Update the interval display text and call the change interval function."""
    seconds = int(value)
    if seconds < 60:
        text = f"Interval: {seconds} seconds"
    else:
        text = "Interval: 1 minute"
    app.interval_var.set(text)
    app.change_move_interval(f"{seconds} seconds" if seconds < 60 else "1 minute")


def setup_navigation_frame(app):
    """Set up the navigation frame with language switcher and settings."""
    colors = get_system_appearance()

    navigation_frame = customtkinter.CTkFrame(
        app,
        fg_color=colors["sidebar"],
        corner_radius=15,
        border_width=1,
        border_color=colors["border"],  # Use theme-aware border color
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
        text_color=colors["text"],
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
        text_color=colors["text_secondary"],
    )
    lang_label.grid(row=0, column=0, padx=20, pady=(0, 10), sticky="w")

    # Language Buttons Frame
    lang_buttons = customtkinter.CTkFrame(lang_frame, fg_color="transparent")
    lang_buttons.grid(row=1, column=0, sticky="ew", padx=20)
    lang_buttons.grid_columnconfigure((0, 1), weight=1)

    # Load flag images
    current_dir = os.path.dirname(os.path.abspath(__file__))
    us_flag_path = os.path.join(current_dir, "images", "us_flag.png")
    es_flag_path = os.path.join(current_dir, "images", "es_flag.png")

    # In the flag loading section of setup_navigation_frame
    try:
        us_img = customtkinter.CTkImage(
            light_image=Image.open(us_flag_path).convert("RGBA"),
            dark_image=Image.open(us_flag_path).convert("RGBA"),
            size=(48, 48),  # Half of 96 for crisp scaling
        )
        es_img = customtkinter.CTkImage(
            light_image=Image.open(es_flag_path).convert("RGBA"),
            dark_image=Image.open(es_flag_path).convert("RGBA"),
            size=(48, 48),  # Half of 96 for crisp scaling
        )
    except FileNotFoundError as e:
        logging.error(f"Could not load flag images: {e}")
        us_img = es_img = None

    app.english_btn = customtkinter.CTkButton(
        lang_buttons,
        text="",
        image=us_img if us_img else None,
        command=lambda: switch_language("en", app),
        fg_color="transparent",
        hover_color=colors["button_hover"],
        width=48,  # Match image size
        height=48,  # Match image size
    )
    app.english_btn.grid(row=0, column=0, padx=5)
    
    app.spanish_btn = customtkinter.CTkButton(
        lang_buttons,
        text="",
        image=es_img if es_img else None,
        command=lambda: switch_language("es", app),
        fg_color="transparent",
        hover_color=colors["button_hover"],
        width=48,  # Match image size
        height=48,  # Match image size
    )
    app.spanish_btn.grid(row=0, column=1, padx=5)

    update_language_buttons(app, app.current_lang)

    # Move Interval Section
    interval_frame = customtkinter.CTkFrame(navigation_frame, fg_color="transparent")
    interval_frame.grid(row=2, column=0, sticky="ew", pady=20)
    interval_frame.grid_columnconfigure(0, weight=1)

    interval_label = customtkinter.CTkLabel(
        interval_frame,
        text="Move Interval",
        font=customtkinter.CTkFont(size=14),
        text_color=colors["text_secondary"],
    )
    interval_label.grid(row=0, column=0, padx=20, pady=(0, 10), sticky="w")

    # Move Interval Slider
    interval_slider = customtkinter.CTkSlider(
        interval_frame,
        from_=5,
        to=60,
        number_of_steps=4,
        command=lambda v: update_interval_text(app, v),
        progress_color=colors["button"],
        button_color=colors["button"],
        button_hover_color=colors["button_hover"],
    )
    interval_slider.grid(row=1, column=0, padx=20, sticky="ew")
    interval_slider.set(5)

    # Interval display text
    interval_text = customtkinter.CTkLabel(
        interval_frame,
        textvariable=app.interval_var,
        font=customtkinter.CTkFont(size=12),
        text_color=colors["text_secondary"],
    )
    interval_text.grid(row=2, column=0, padx=20, pady=(5, 0), sticky="w")

    # Font Size Section
    font_frame = customtkinter.CTkFrame(navigation_frame, fg_color="transparent")
    font_frame.grid(row=3, column=0, sticky="ew", pady=20)
    font_frame.grid_columnconfigure(0, weight=1)

    font_label = customtkinter.CTkLabel(
        font_frame,
        text="Font Size",
        font=customtkinter.CTkFont(size=14),
        text_color=colors["text_secondary"],
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
        fg_color=colors["button"],
        button_color=colors["button_hover"],
    )
    font_dropdown.grid(row=1, column=0, padx=20, sticky="ew")

    return navigation_frame


def setup_main_frame(app):
    """Set up the main content frame."""
    colors = get_system_appearance()

    main_frame = customtkinter.CTkFrame(
        app,
        fg_color=colors["bg"],
        corner_radius=15,
        border_width=1,
        border_color=colors["border"],  # Use theme-aware border color
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

    for i, (var, size) in enumerate(
        [(app.text_var, 28), (app.counter_var, 20), (app.time_var, 20)]
    ):
        label = customtkinter.CTkLabel(
            labels_frame,
            textvariable=var,
            font=customtkinter.CTkFont(size=size, weight="bold"),
            text_color=colors["text"],
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
        fg_color=colors["button"],
        hover_color=colors["button_hover"],
        height=50,
        corner_radius=12,
    )
    app.start_button.grid(row=0, column=0, padx=15, sticky="ew")

    app.stop_button = customtkinter.CTkButton(
        button_frame,
        text=app.languages["stop"],
        command=app.stop_moving,
        font=customtkinter.CTkFont(size=18, weight="bold"),
        fg_color=colors["stop"],
        hover_color=colors["stop_hover"],
        height=50,
        corner_radius=12,
        state="disabled",
    )
    app.stop_button.grid(row=0, column=1, padx=15, sticky="ew")

    return main_frame

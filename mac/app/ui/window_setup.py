import tkinter as tk
import customtkinter
import os
from app.config import APP_NAME, MIN_WINDOW_SIZE
from app.utils import load_language, update_labels

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

    # Create main frames with translucent effect
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

    # Title centered
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

    # Text Scale Section
    scale_frame = customtkinter.CTkFrame(navigation_frame, fg_color="transparent")
    scale_frame.grid(row=3, column=0, sticky="ew", pady=20)
    scale_frame.grid_columnconfigure(0, weight=1)

    scale_label = customtkinter.CTkLabel(
        scale_frame,
        text="Text Scale",
        font=customtkinter.CTkFont(size=14),
        text_color=COLORS["text_secondary"]
    )
    scale_label.grid(row=0, column=0, padx=20, pady=(0, 10), sticky="w")

    scale_slider = customtkinter.CTkSlider(
        scale_frame,
        from_=80,
        to=120,
        number_of_steps=4,
        command=lambda v: app.change_scaling_event(f"{int(v)}%"),
        progress_color=COLORS["button"],
        button_color=COLORS["button"],
        button_hover_color=COLORS["button_hover"]
    )
    scale_slider.grid(row=1, column=0, padx=20, sticky="ew")
    scale_slider.set(100)

    # Main content frame
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

    return app, {
        "navigation_frame": navigation_frame,
        "main_frame": main_frame
    }
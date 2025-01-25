import tkinter as tk
from tkinter import ttk
from app.config import APP_NAME, MIN_WINDOW_SIZE
from app.utils import load_flag_image, switch_language, update_labels

def setup_main_window(app):
    """Set up the main application window."""
    root = tk.Tk()
    root.title(APP_NAME)
    root.minsize(*MIN_WINDOW_SIZE)

    # Setup window bindings
    setup_window_bindings(app, root)

    # Main frame
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Configure grid weights
    for i in range(2):
        root.columnconfigure(0, weight=1)
        root.rowconfigure(i, weight=1)

    # Create language selection frame
    create_language_frame(app, main_frame)

    # Create main content frame
    create_main_content(app, main_frame)

    # Collect UI components
    ui_components = {
        'root': root,
        'main_frame': main_frame
    }

    return root, ui_components

def setup_window_bindings(app, root):
    """Configure window event bindings."""
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.bind("<Unmap>", lambda e: app.handle_minimize())
    root.bind("<Map>", lambda e: app.handle_restore())

def create_language_frame(app, main_frame):
    """Create language selection buttons."""
    lang_frame = ttk.Frame(main_frame.master, padding="5")
    lang_frame.grid(row=0, column=0, pady=10, sticky="ew")

    # Configure frame columns
    for i in range(2):
        lang_frame.columnconfigure(i, weight=1)

    # Create flag buttons
    flags = [
        ("us", "en"),
        ("spain", "es")
    ]

    for i, (flag_name, lang_code) in enumerate(flags):
        flag_image = load_flag_image(f"https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/32px-Flag_of_the_United_States.svg.png" 
                                     if flag_name == "us" else 
                                     "https://upload.wikimedia.org/wikipedia/en/thumb/9/9a/Flag_of_Spain.svg/32px-Flag_of_Spain.svg.png")
        
        btn = tk.Button(
            lang_frame, 
            image=flag_image,
            command=lambda l=lang_code: switch_language(l, app),
            relief="flat",
            bd=0,
            cursor="hand2",
            highlightthickness=0,
            bg=main_frame.master['bg'],
            activebackground=main_frame.master['bg']
        )
        btn.image = flag_image  # Keep a reference to prevent garbage collection
        btn.grid(row=0, column=i, padx=5, pady=5)

def create_main_content(app, main_frame):
    """Create main application content."""
    # Create and configure StringVars
    app.text_var = tk.StringVar(value=app.languages["press_start"])
    app.counter_var = tk.StringVar(value=app.languages["mouse_not_moved"])
    app.time_var = tk.StringVar(value=app.languages["not_started_yet"])

    # Create labels
    labels = [
        (app.text_var, 0),
        (app.counter_var, 1),
        (app.time_var, 2)
    ]

    for var, row in labels:
        ttk.Label(
            main_frame,
            textvariable=var,
            anchor="center"
        ).grid(row=row, column=0, columnspan=2, pady=10, sticky="ew")

    # Create buttons
    app.start_button = ttk.Button(
        main_frame,
        text=app.languages["start"],
        command=app.start_moving
    )
    app.stop_button = ttk.Button(
        main_frame,
        text=app.languages["stop"],
        command=app.stop_moving
    )

    app.start_button.grid(row=3, column=0, padx=5, pady=10, sticky="ew")
    app.stop_button.grid(row=3, column=1, padx=5, pady=10, sticky="ew")
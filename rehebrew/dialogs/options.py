"""
Options dialog for ReHebrew settings
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable

from ..utils import ICO_FILE


def show_options_dialog(
    current_shortcut: str,
    show_notifications: bool,
    on_save: Callable[[str, bool], None]
) -> None:
    """
    Show the Options dialog.
    
    Args:
        current_shortcut: Current keyboard shortcut
        show_notifications: Current notification setting
        on_save: Callback function with (new_shortcut, show_notifications)
    """
    dialog = tk.Tk()
    dialog.title("ReHebrew Options")
    dialog.geometry("420x220")
    dialog.resizable(False, False)
    dialog.attributes('-topmost', True)
    
    # Set window icon
    if ICO_FILE.exists():
        try:
            dialog.iconbitmap(str(ICO_FILE))
        except Exception:
            pass
    
    # Center the dialog
    x = (dialog.winfo_screenwidth() - 420) // 2
    y = (dialog.winfo_screenheight() - 220) // 2
    dialog.geometry(f"420x220+{x}+{y}")
    
    main = ttk.Frame(dialog, padding="20")
    main.pack(fill=tk.BOTH, expand=True)
    
    # Shortcut section
    shortcut_frame = ttk.LabelFrame(main, text="Keyboard Shortcut", padding="10")
    shortcut_frame.pack(fill=tk.X, pady=(0, 10))
    
    row = ttk.Frame(shortcut_frame)
    row.pack(fill=tk.X)
    ttk.Label(row, text="Shortcut:").pack(side=tk.LEFT)
    
    shortcut_var = tk.StringVar(value=current_shortcut)
    shortcut_entry = ttk.Entry(row, textvariable=shortcut_var, width=20)
    shortcut_entry.pack(side=tk.LEFT, padx=(10, 0))
    
    # Preset buttons
    preset_frame = ttk.Frame(main)
    preset_frame.pack(fill=tk.X, pady=(0, 10))
    ttk.Label(preset_frame, text="Presets:").pack(side=tk.LEFT, padx=(0, 10))
    
    presets = [
        ("Ctrl+Shift+H", "ctrl+shift+h"),
        ("Ctrl+Alt+H", "ctrl+alt+h"),
        ("Ctrl+`", "ctrl+`")
    ]
    
    for label, value in presets:
        ttk.Button(
            preset_frame,
            text=label,
            command=lambda v=value: shortcut_var.set(v),
            width=12
        ).pack(side=tk.LEFT, padx=3)
    
    # Notification checkbox
    notify_var = tk.BooleanVar(value=show_notifications)
    ttk.Checkbutton(
        main,
        text="Show notifications",
        variable=notify_var
    ).pack(anchor=tk.W)
    
    # Button frame
    btn_frame = ttk.Frame(main)
    btn_frame.pack(fill=tk.X, pady=(15, 0), side=tk.BOTTOM)
    
    def save():
        new_shortcut = shortcut_var.get().strip().lower()
        if not new_shortcut:
            messagebox.showerror("Error", "Shortcut cannot be empty")
            return
        
        on_save(new_shortcut, notify_var.get())
        dialog.destroy()
    
    ttk.Button(
        btn_frame,
        text="Cancel",
        command=dialog.destroy,
        width=10
    ).pack(side=tk.RIGHT, padx=(5, 0))
    
    ttk.Button(
        btn_frame,
        text="Save",
        command=save,
        width=10
    ).pack(side=tk.RIGHT)
    
    dialog.mainloop()

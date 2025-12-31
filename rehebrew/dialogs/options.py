"""
Options dialog for ReHebrew settings
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable

from ..utils import ICO_FILE


def show_options_dialog(
    current_shortcut: str,
    current_shortcut_english: str,
    show_notifications: bool,
    on_save: Callable[[str, str, bool], None]
) -> None:
    """
    Show the Options dialog.
    
    Args:
        current_shortcut: Current keyboard shortcut for Hebrew
        current_shortcut_english: Current keyboard shortcut for English
        show_notifications: Current notification setting
        on_save: Callback function with (shortcut_hebrew, shortcut_english, show_notifications)
    """
    dialog = tk.Tk()
    dialog.title("ReHebrew Options")
    dialog.geometry("450x320")
    dialog.resizable(False, False)
    dialog.attributes('-topmost', True)
    
    # Set window icon
    if ICO_FILE.exists():
        try:
            dialog.iconbitmap(str(ICO_FILE))
        except Exception:
            pass
    
    # Center the dialog
    x = (dialog.winfo_screenwidth() - 450) // 2
    y = (dialog.winfo_screenheight() - 320) // 2
    dialog.geometry(f"450x320+{x}+{y}")
    
    main = ttk.Frame(dialog, padding="20")
    main.pack(fill=tk.BOTH, expand=True)
    
    # Hebrew Shortcut section
    hebrew_frame = ttk.LabelFrame(main, text="English → Hebrew (convert gibberish to Hebrew)", padding="10")
    hebrew_frame.pack(fill=tk.X, pady=(0, 10))
    
    row1 = ttk.Frame(hebrew_frame)
    row1.pack(fill=tk.X)
    ttk.Label(row1, text="Shortcut:").pack(side=tk.LEFT)
    
    shortcut_var = tk.StringVar(value=current_shortcut)
    shortcut_entry = ttk.Entry(row1, textvariable=shortcut_var, width=20)
    shortcut_entry.pack(side=tk.LEFT, padx=(10, 0))
    
    preset_frame1 = ttk.Frame(hebrew_frame)
    preset_frame1.pack(fill=tk.X, pady=(5, 0))
    
    presets_hebrew = [
        ("Ctrl+Shift+H", "ctrl+shift+h"),
        ("Ctrl+Alt+H", "ctrl+alt+h"),
    ]
    
    for label, value in presets_hebrew:
        ttk.Button(
            preset_frame1,
            text=label,
            command=lambda v=value: shortcut_var.set(v),
            width=14
        ).pack(side=tk.LEFT, padx=3)
    
    # English Shortcut section
    english_frame = ttk.LabelFrame(main, text="Hebrew → English (convert gibberish to English)", padding="10")
    english_frame.pack(fill=tk.X, pady=(0, 10))
    
    row2 = ttk.Frame(english_frame)
    row2.pack(fill=tk.X)
    ttk.Label(row2, text="Shortcut:").pack(side=tk.LEFT)
    
    shortcut_english_var = tk.StringVar(value=current_shortcut_english)
    shortcut_english_entry = ttk.Entry(row2, textvariable=shortcut_english_var, width=20)
    shortcut_english_entry.pack(side=tk.LEFT, padx=(10, 0))
    
    preset_frame2 = ttk.Frame(english_frame)
    preset_frame2.pack(fill=tk.X, pady=(5, 0))
    
    presets_english = [
        ("Ctrl+Shift+E", "ctrl+shift+e"),
        ("Ctrl+Alt+E", "ctrl+alt+e"),
    ]
    
    for label, value in presets_english:
        ttk.Button(
            preset_frame2,
            text=label,
            command=lambda v=value: shortcut_english_var.set(v),
            width=14
        ).pack(side=tk.LEFT, padx=3)
    
    # Notification checkbox
    notify_var = tk.BooleanVar(value=show_notifications)
    ttk.Checkbutton(
        main,
        text="Show notifications",
        variable=notify_var
    ).pack(anchor=tk.W, pady=(5, 0))
    
    # Button frame
    btn_frame = ttk.Frame(main)
    btn_frame.pack(fill=tk.X, pady=(15, 0), side=tk.BOTTOM)
    
    def save():
        new_shortcut = shortcut_var.get().strip().lower()
        new_shortcut_english = shortcut_english_var.get().strip().lower()
        
        if not new_shortcut:
            messagebox.showerror("Error", "Hebrew shortcut cannot be empty")
            return
        if not new_shortcut_english:
            messagebox.showerror("Error", "English shortcut cannot be empty")
            return
        if new_shortcut == new_shortcut_english:
            messagebox.showerror("Error", "Shortcuts must be different")
            return
        
        on_save(new_shortcut, new_shortcut_english, notify_var.get())
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

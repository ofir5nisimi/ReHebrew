"""
About dialog for ReHebrew
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional
from PIL import Image

from .. import __version__, __author__, __app_name__
from ..utils import ICO_FILE


def show_about_dialog(
    shortcut: str,
    shortcut_english: str,
    logo_image: Optional[Image.Image] = None
) -> None:
    """
    Show the About dialog.
    
    Args:
        shortcut: Current keyboard shortcut for Hebrew
        shortcut_english: Current keyboard shortcut for English
        logo_image: Optional logo image to display
    """
    from PIL import ImageTk
    
    dialog = tk.Tk()
    dialog.title(f"About {__app_name__}")
    dialog.resizable(False, False)
    dialog.attributes('-topmost', True)
    dialog.configure(bg='#ffffff')
    
    # Set window icon
    if ICO_FILE.exists():
        try:
            dialog.iconbitmap(str(ICO_FILE))
        except Exception:
            pass
    
    # Custom styles
    style = ttk.Style()
    style.configure('About.TFrame', background='#ffffff')
    style.configure('About.TLabel', background='#ffffff')
    style.configure('Title.TLabel', background='#ffffff', font=('Segoe UI', 24, 'bold'))
    style.configure('Version.TLabel', background='#ffffff', font=('Segoe UI', 11))
    style.configure('Desc.TLabel', background='#ffffff', font=('Segoe UI', 10))
    style.configure('Author.TLabel', background='#ffffff', font=('Segoe UI', 10, 'italic'))
    style.configure('About.TButton', font=('Segoe UI', 10), padding=(20, 10))
    
    main = ttk.Frame(dialog, padding="30", style='About.TFrame')
    main.pack(fill=tk.BOTH, expand=True)
    
    # App logo
    icon_frame = ttk.Frame(main, style='About.TFrame')
    icon_frame.pack(pady=(0, 10))
    
    # Store reference to prevent garbage collection
    _logo_photo = None
    
    if logo_image:
        logo_resized = logo_image.resize((100, 100), Image.Resampling.LANCZOS)
        _logo_photo = ImageTk.PhotoImage(logo_resized)
        logo_label = ttk.Label(icon_frame, image=_logo_photo, style='About.TLabel')
        logo_label.image = _logo_photo  # Keep reference
        logo_label.pack()
    else:
        # Fallback to canvas if no logo
        canvas = tk.Canvas(icon_frame, width=80, height=80, bg='#ffffff', highlightthickness=0)
        canvas.pack()
        canvas.create_oval(5, 5, 75, 75, fill='#0078D4', outline='#005A9E', width=2)
        canvas.create_text(40, 38, text="עב", font=('Arial', 28, 'bold'), fill='white')
    
    # App name
    ttk.Label(main, text=__app_name__, style='Title.TLabel').pack(pady=(5, 5))
    
    # Version
    ttk.Label(main, text=f"Version {__version__}", style='Version.TLabel').pack()
    
    # Tagline
    ttk.Label(
        main,
        text="Hebrew Text Converter",
        style='Desc.TLabel',
        foreground='#666666'
    ).pack(pady=(2, 20))
    
    # Description
    desc_frame = ttk.Frame(main, style='About.TFrame')
    desc_frame.pack(fill=tk.X, pady=(0, 20))
    
    desc_text = "Convert text typed with the wrong keyboard layout\nusing simple keyboard shortcuts."
    ttk.Label(desc_frame, text=desc_text, style='Desc.TLabel', justify=tk.CENTER).pack()
    
    shortcuts_text = f"{shortcut.upper()} → Hebrew\n{shortcut_english.upper()} → English"
    ttk.Label(
        desc_frame,
        text=shortcuts_text,
        style='Desc.TLabel',
        foreground='#0078D4',
        font=('Segoe UI', 10, 'bold'),
        justify=tk.CENTER
    ).pack(pady=(8, 0))
    
    # Separator
    ttk.Separator(main, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(5, 15))
    
    # Author info
    ttk.Label(main, text=f"Created by {__author__}", style='Author.TLabel').pack()
    ttk.Label(
        main,
        text="© 2025 All Rights Reserved",
        style='Desc.TLabel',
        foreground='#999999',
        font=('Segoe UI', 9)
    ).pack(pady=(3, 0))
    
    # Close button
    btn_frame = ttk.Frame(main, style='About.TFrame')
    btn_frame.pack(pady=(20, 10))
    ttk.Button(
        btn_frame,
        text="Close",
        command=dialog.destroy,
        style='About.TButton',
        width=12
    ).pack()
    
    # Update and center after all widgets are added
    dialog.update_idletasks()
    width = dialog.winfo_reqwidth()
    height = dialog.winfo_reqheight()
    x = (dialog.winfo_screenwidth() - width) // 2
    y = (dialog.winfo_screenheight() - height) // 2
    dialog.geometry(f"{width}x{height}+{x}+{y}")
    
    dialog.mainloop()

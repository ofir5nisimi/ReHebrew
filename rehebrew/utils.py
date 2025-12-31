"""
Path utilities and helper functions
"""

import sys
import ctypes
from pathlib import Path


def get_base_path() -> Path:
    """
    Get the base path for resources.
    Handles PyInstaller bundled app where resources are in a temp folder.
    """
    if getattr(sys, 'frozen', False):
        # Running as bundled exe - resources are in _MEIPASS temp folder
        return Path(sys._MEIPASS)
    # Running as script - resources are relative to package
    return Path(__file__).parent.parent


def get_app_path() -> Path:
    """
    Get the app directory (for config file and user data).
    This is where the exe is located, or the project root for development.
    """
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).parent.parent


def ensure_single_instance(mutex_name: str = "ReHebrew_Mutex") -> bool:
    """
    Ensure only one instance of the app is running.
    Returns True if this is the only instance, False if another is running.
    """
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
    if ctypes.windll.kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
        return False
    return True


# Pre-computed paths for easy access
BASE_PATH = get_base_path()
APP_PATH = get_app_path()
ASSETS_DIR = BASE_PATH / "assets"
LOGO_FILE = ASSETS_DIR / "1767170448668.jpg"
ICO_FILE = ASSETS_DIR / "icon.ico"

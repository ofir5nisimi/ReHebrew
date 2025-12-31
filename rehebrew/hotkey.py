"""
Windows global hotkey registration and handling
"""

import ctypes
from ctypes import wintypes
import threading
import time
from typing import Callable, Optional

from .constants import (
    MOD_ALT, MOD_CONTROL, MOD_SHIFT, MOD_WIN, MOD_NOREPEAT,
    WM_HOTKEY, HOTKEY_ID, VK_CODES
)


# Windows API
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32


def parse_shortcut(shortcut_str: str) -> tuple:
    """
    Parse a shortcut string into modifiers and virtual key code.
    
    Args:
        shortcut_str: Shortcut like "ctrl+shift+h" or "ctrl+alt+f1"
        
    Returns:
        Tuple of (modifiers, virtual_key_code)
    """
    modifiers = MOD_NOREPEAT  # Prevent repeat when held
    vk = 0
    
    parts = shortcut_str.lower().replace(' ', '').split('+')
    
    for part in parts:
        if part in ('ctrl', 'control'):
            modifiers |= MOD_CONTROL
        elif part == 'shift':
            modifiers |= MOD_SHIFT
        elif part == 'alt':
            modifiers |= MOD_ALT
        elif part in ('win', 'windows', 'super'):
            modifiers |= MOD_WIN
        elif part in VK_CODES:
            vk = VK_CODES[part]
    
    return modifiers, vk


class HotkeyListener:
    """
    Manages Windows global hotkey registration and listening.
    Runs in a separate thread to avoid blocking the main UI.
    """
    
    def __init__(self, shortcut: str, callback: Callable):
        """
        Initialize the hotkey listener.
        
        Args:
            shortcut: Shortcut string like "ctrl+shift+h"
            callback: Function to call when hotkey is pressed
        """
        self.shortcut = shortcut
        self.callback = callback
        self.running = False
        self._thread: Optional[threading.Thread] = None
    
    def start(self) -> bool:
        """Start listening for the hotkey in a background thread"""
        if self._thread and self._thread.is_alive():
            return False
        
        self.running = True
        self._thread = threading.Thread(target=self._listen, daemon=True)
        self._thread.start()
        return True
    
    def stop(self) -> None:
        """Stop listening for the hotkey"""
        self.running = False
        if self._thread:
            self._thread.join(timeout=1.0)
    
    def _listen(self) -> None:
        """Internal method that runs in the listener thread"""
        modifiers, vk = parse_shortcut(self.shortcut)
        
        if vk == 0:
            print(f"Invalid shortcut: {self.shortcut}")
            return
        
        # Register the hotkey
        if not user32.RegisterHotKey(None, HOTKEY_ID, modifiers, vk):
            error = kernel32.GetLastError()
            print(f"Failed to register hotkey (error {error})")
            return
        
        try:
            msg = wintypes.MSG()
            while self.running:
                # Use PeekMessage to allow checking self.running
                if user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 1):  # PM_REMOVE = 1
                    if msg.message == WM_HOTKEY and msg.wParam == HOTKEY_ID:
                        # Handle hotkey in a separate thread to avoid blocking
                        threading.Thread(target=self.callback, daemon=True).start()
                else:
                    time.sleep(0.01)  # Small sleep to prevent CPU spinning
        finally:
            user32.UnregisterHotKey(None, HOTKEY_ID)

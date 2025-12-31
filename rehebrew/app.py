"""
Main ReHebrew application class
"""

import os
import sys
import time
import threading
import winreg
from typing import Optional

import pyperclip
from plyer import notification

from .config import Config
from .converter import convert_to_hebrew, convert_to_english
from .keyboard import send_ctrl_c, send_ctrl_v
from .hotkey import HotkeyListener
from .tray import TrayIcon
from .dialogs import show_about_dialog, show_options_dialog
from .constants import HOTKEY_ID, HOTKEY_ID_ENGLISH


class ReHebrew:
    """Main application class for ReHebrew"""
    
    def __init__(self):
        self.config = Config()
        self.running = True
        self._hotkey_listener: Optional[HotkeyListener] = None
        self._hotkey_listener_english: Optional[HotkeyListener] = None
        self._tray: Optional[TrayIcon] = None
    
    def do_conversion(self) -> None:
        """Perform the text conversion to Hebrew (copy, convert, paste)"""
        self._do_conversion_internal(convert_to_hebrew, "Hebrew")
    
    def do_conversion_english(self) -> None:
        """Perform the text conversion to English (copy, convert, paste)"""
        self._do_conversion_internal(convert_to_english, "English")
    
    def _do_conversion_internal(self, converter_func, direction: str) -> None:
        """Internal conversion logic used by both directions"""
        if not self.config.enabled:
            return
        
        # Small delay to let hotkey keys be released
        time.sleep(0.2)
        
        # Save original clipboard
        try:
            original = pyperclip.paste()
        except Exception:
            original = ""
        
        # Copy selected text
        send_ctrl_c()
        time.sleep(0.15)
        
        # Get copied text
        try:
            text = pyperclip.paste()
        except Exception:
            text = ""
        
        if not text or text == original:
            self._notify("ReHebrew", "No text selected.", 2)
            return
        
        # Convert
        converted, count = converter_func(text)
        
        if count == 0:
            self._notify("ReHebrew", "No convertible characters.", 2)
            return
        
        # Paste converted text
        pyperclip.copy(converted)
        send_ctrl_v()
    
    def _notify(self, title: str, message: str, timeout: int = 3) -> None:
        """Show a notification if enabled"""
        if self.config.show_notifications:
            try:
                notification.notify(
                    title=title,
                    message=message,
                    app_name='ReHebrew',
                    timeout=timeout
                )
            except Exception:
                pass
    
    def _toggle_enabled(self, icon=None, item=None) -> None:
        """Toggle enabled state"""
        self.config.enabled = not self.config.enabled
        self.config.save()
        if self._tray:
            self._tray.update_icon(self.config.enabled)
        status = 'enabled' if self.config.enabled else 'disabled'
        self._notify("ReHebrew", f"ReHebrew {status}")
    
    def _is_enabled(self, item=None) -> bool:
        """Return current enabled state"""
        return self.config.enabled
    
    def _toggle_autostart(self, icon=None, item=None) -> None:
        """Toggle auto-start with Windows"""
        self.config.auto_start = not self.config.auto_start
        self.config.save()
        self._setup_autostart()
    
    def _is_autostart(self, item=None) -> bool:
        """Return current auto-start state"""
        return self.config.auto_start
    
    def _setup_autostart(self) -> None:
        """Configure Windows auto-start registry entry"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            
            if self.config.auto_start:
                # Add to startup
                exe_path = sys.executable
                if getattr(sys, 'frozen', False):
                    exe_path = sys.executable
                    winreg.SetValueEx(key, 'ReHebrew', 0, winreg.REG_SZ, f'"{exe_path}"')
                else:
                    script_path = os.path.abspath(sys.argv[0])
                    winreg.SetValueEx(
                        key, 'ReHebrew', 0, winreg.REG_SZ,
                        f'"{exe_path}" "{script_path}"'
                    )
            else:
                # Remove from startup
                try:
                    winreg.DeleteValue(key, 'ReHebrew')
                except FileNotFoundError:
                    pass
            
            winreg.CloseKey(key)
        except Exception:
            pass
    
    def _show_about(self, icon=None, item=None) -> None:
        """Show About dialog in a separate thread"""
        logo = self._tray.logo_image if self._tray else None
        threading.Thread(
            target=show_about_dialog,
            args=(self.config.shortcut, self.config.shortcut_english, logo),
            daemon=True
        ).start()
    
    def _show_options(self, icon=None, item=None) -> None:
        """Show Options dialog in a separate thread"""
        def on_save(new_shortcut: str, new_shortcut_english: str, show_notifications: bool) -> None:
            old_shortcut = self.config.shortcut
            old_shortcut_english = self.config.shortcut_english
            
            self.config.shortcut = new_shortcut
            self.config.shortcut_english = new_shortcut_english
            self.config.show_notifications = show_notifications
            self.config.save()
            
            # Update Hebrew hotkey if changed
            if new_shortcut != old_shortcut and self._hotkey_listener:
                if self._hotkey_listener.update_shortcut(new_shortcut):
                    self._notify("ReHebrew", f"Hebrew shortcut: {new_shortcut.upper()}", 3)
                else:
                    self._notify("ReHebrew", f"Failed to set {new_shortcut.upper()}", 5)
            
            # Update English hotkey if changed
            if new_shortcut_english != old_shortcut_english and self._hotkey_listener_english:
                if self._hotkey_listener_english.update_shortcut(new_shortcut_english):
                    self._notify("ReHebrew", f"English shortcut: {new_shortcut_english.upper()}", 3)
                else:
                    self._notify("ReHebrew", f"Failed to set {new_shortcut_english.upper()}", 5)
        
        threading.Thread(
            target=show_options_dialog,
            args=(
                self.config.shortcut,
                self.config.shortcut_english,
                self.config.show_notifications,
                on_save
            ),
            daemon=True
        ).start()
    
    def _quit(self, icon=None, item=None) -> None:
        """Quit the application"""
        self.running = False
        if self._hotkey_listener:
            self._hotkey_listener.stop()
        if self._hotkey_listener_english:
            self._hotkey_listener_english.stop()
        if self._tray:
            self._tray.stop()
    
    def run(self) -> None:
        """Start the application"""
        # Start hotkey listener for Hebrew conversion
        self._hotkey_listener = HotkeyListener(
            self.config.shortcut,
            self.do_conversion,
            HOTKEY_ID
        )
        self._hotkey_listener.start()
        
        # Start hotkey listener for English conversion
        self._hotkey_listener_english = HotkeyListener(
            self.config.shortcut_english,
            self.do_conversion_english,
            HOTKEY_ID_ENGLISH
        )
        self._hotkey_listener_english.start()
        
        # Create tray icon
        self._tray = TrayIcon(
            on_toggle_enabled=self._toggle_enabled,
            on_options=self._show_options,
            on_toggle_autostart=self._toggle_autostart,
            on_about=self._show_about,
            on_exit=self._quit,
            is_enabled=self._is_enabled,
            is_autostart=self._is_autostart
        )
        
        # Show startup notification
        self._notify(
            "ReHebrew",
            f"Running in background.\n"
            f"{self.config.shortcut.upper()} → Hebrew\n"
            f"{self.config.shortcut_english.upper()} → English",
            3
        )
        
        # Run tray icon (blocking)
        self._tray.run()

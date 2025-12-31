"""
Keyboard input simulation using Windows SendInput API
"""

import ctypes
from ctypes import wintypes

from .constants import (
    INPUT_KEYBOARD, KEYEVENTF_KEYUP,
    VK_CONTROL, VK_C, VK_V
)


# Windows API
user32 = ctypes.windll.user32


class KEYBDINPUT(ctypes.Structure):
    """Structure for keyboard input"""
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]


class INPUT(ctypes.Structure):
    """Structure for SendInput"""
    _fields_ = [
        ("type", wintypes.DWORD),
        ("ki", KEYBDINPUT),
        ("padding", ctypes.c_ubyte * 8)
    ]


def _make_input(vk: int, flags: int = 0) -> INPUT:
    """Create an INPUT structure for a key press/release"""
    return INPUT(
        type=INPUT_KEYBOARD,
        ki=KEYBDINPUT(
            wVk=vk,
            wScan=0,
            dwFlags=flags,
            time=0,
            dwExtraInfo=None
        )
    )


def send_key_combo(modifier: int, key: int) -> None:
    """
    Send a key combination (modifier + key).
    
    Args:
        modifier: Virtual key code for modifier (e.g., VK_CONTROL)
        key: Virtual key code for the main key
    """
    inputs = (INPUT * 4)(
        _make_input(modifier),           # Press modifier
        _make_input(key),                 # Press key
        _make_input(key, KEYEVENTF_KEYUP),      # Release key
        _make_input(modifier, KEYEVENTF_KEYUP)  # Release modifier
    )
    user32.SendInput(4, ctypes.byref(inputs), ctypes.sizeof(INPUT))


def send_ctrl_c() -> None:
    """Send Ctrl+C (copy) using SendInput"""
    send_key_combo(VK_CONTROL, VK_C)


def send_ctrl_v() -> None:
    """Send Ctrl+V (paste) using SendInput"""
    send_key_combo(VK_CONTROL, VK_V)

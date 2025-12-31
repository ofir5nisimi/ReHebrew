"""
ReHebrew - Convert English-layout gibberish to Hebrew text
A Windows system tray application by Ofir Nisimi
"""

__version__ = "1.0.0"
__author__ = "Ofir Nisimi"
__app_name__ = "ReHebrew"

from .app import ReHebrew
from .main import main

__all__ = ['ReHebrew', 'main', '__version__', '__author__', '__app_name__']

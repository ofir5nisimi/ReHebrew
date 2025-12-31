"""
ReHebrew - Entry point for PyInstaller

This simple wrapper allows PyInstaller to bundle the package correctly.
Run with: python main.py
Build with: pyinstaller --onefile --windowed --name=ReHebrew --icon=assets/icon.ico --add-data "assets;assets" main.py
"""

from rehebrew import main

if __name__ == '__main__':
    main()

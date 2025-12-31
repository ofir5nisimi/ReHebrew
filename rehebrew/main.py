"""
Main entry point for ReHebrew application
"""

import sys

from .utils import ensure_single_instance
from .app import ReHebrew


def main() -> None:
    """Main entry point"""
    # Ensure only one instance is running
    if not ensure_single_instance():
        sys.exit(0)
    
    # Run the application
    app = ReHebrew()
    app.run()


if __name__ == '__main__':
    main()

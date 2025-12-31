"""
Configuration management for ReHebrew
"""

import json
from pathlib import Path
from typing import Dict, Any

from .utils import APP_PATH


# Default configuration values
DEFAULT_CONFIG: Dict[str, Any] = {
    "shortcut": "ctrl+shift+h",
    "shortcut_english": "ctrl+shift+e",
    "auto_start": False,
    "enabled": True,
    "show_notifications": True
}

CONFIG_FILE = APP_PATH / "config.json"


class Config:
    """Configuration manager for ReHebrew settings"""
    
    def __init__(self, config_file: Path = None):
        self.config_file = config_file or CONFIG_FILE
        self._config = self._load()
    
    def _load(self) -> Dict[str, Any]:
        """Load configuration from file, merging with defaults"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    return {**DEFAULT_CONFIG, **user_config}
            except (json.JSONDecodeError, IOError):
                pass
        return DEFAULT_CONFIG.copy()
    
    def save(self) -> bool:
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2)
            return True
        except IOError:
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value"""
        self._config[key] = value
    
    def __getitem__(self, key: str) -> Any:
        return self._config[key]
    
    def __setitem__(self, key: str, value: Any) -> None:
        self._config[key] = value
    
    @property
    def shortcut(self) -> str:
        return self._config.get('shortcut', 'ctrl+shift+h')
    
    @shortcut.setter
    def shortcut(self, value: str) -> None:
        self._config['shortcut'] = value
    
    @property
    def shortcut_english(self) -> str:
        return self._config.get('shortcut_english', 'ctrl+shift+e')
    
    @shortcut_english.setter
    def shortcut_english(self, value: str) -> None:
        self._config['shortcut_english'] = value
    
    @property
    def enabled(self) -> bool:
        return self._config.get('enabled', True)
    
    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._config['enabled'] = value
    
    @property
    def auto_start(self) -> bool:
        return self._config.get('auto_start', False)
    
    @auto_start.setter
    def auto_start(self, value: bool) -> None:
        self._config['auto_start'] = value
    
    @property
    def show_notifications(self) -> bool:
        return self._config.get('show_notifications', True)
    
    @show_notifications.setter
    def show_notifications(self, value: bool) -> None:
        self._config['show_notifications'] = value

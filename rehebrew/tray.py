"""
System tray icon and menu management
"""

from typing import Callable, Optional
from PIL import Image

from pystray import Icon, Menu, MenuItem

from .utils import LOGO_FILE


class TrayIcon:
    """Manages the system tray icon and menu"""
    
    def __init__(
        self,
        on_toggle_enabled: Callable,
        on_options: Callable,
        on_toggle_autostart: Callable,
        on_about: Callable,
        on_exit: Callable,
        is_enabled: Callable,
        is_autostart: Callable
    ):
        """
        Initialize the tray icon.
        
        Args:
            on_toggle_enabled: Callback when Enable/Disable is clicked
            on_options: Callback when Options is clicked
            on_toggle_autostart: Callback when Start with Windows is clicked
            on_about: Callback when About is clicked
            on_exit: Callback when Exit is clicked
            is_enabled: Function that returns current enabled state
            is_autostart: Function that returns current autostart state
        """
        self.on_toggle_enabled = on_toggle_enabled
        self.on_options = on_options
        self.on_toggle_autostart = on_toggle_autostart
        self.on_about = on_about
        self.on_exit = on_exit
        self.is_enabled = is_enabled
        self.is_autostart = is_autostart
        
        self._logo_image = self._load_logo()
        self._icon: Optional[Icon] = None
    
    def _load_logo(self) -> Optional[Image.Image]:
        """Load the logo image from assets"""
        if LOGO_FILE.exists():
            try:
                return Image.open(LOGO_FILE).convert('RGBA')
            except Exception:
                pass
        return None
    
    def create_icon_image(self, enabled: bool = True) -> Image.Image:
        """
        Create the tray icon image.
        
        Args:
            enabled: Whether the app is enabled (affects icon appearance)
            
        Returns:
            PIL Image for the tray icon
        """
        size = 64
        
        # Use custom logo if available
        if self._logo_image:
            img = self._logo_image.resize((size, size), Image.Resampling.LANCZOS)
            if not enabled:
                # Convert to grayscale for disabled state
                img = img.convert('LA').convert('RGBA')
            return img
        
        # Fallback to generated icon
        from PIL import ImageDraw, ImageFont
        
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse(
            [2, 2, size-2, size-2],
            fill=(0, 120, 215) if enabled else (128, 128, 128)
        )
        
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except Exception:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), "ע", font=font)
        x = (size - bbox[2] + bbox[0]) // 2
        y = (size - bbox[3] + bbox[1]) // 2 - 4
        draw.text((x, y), "ע", fill='white', font=font)
        
        return img
    
    def _create_menu(self) -> Menu:
        """Create the tray icon context menu"""
        return Menu(
            MenuItem('Enable ReHebrew', self.on_toggle_enabled, checked=self.is_enabled),
            Menu.SEPARATOR,
            MenuItem('Options...', self.on_options),
            MenuItem('Start with Windows', self.on_toggle_autostart, checked=self.is_autostart),
            Menu.SEPARATOR,
            MenuItem('About', self.on_about),
            MenuItem('Exit', self.on_exit)
        )
    
    def update_icon(self, enabled: bool) -> None:
        """Update the icon appearance based on enabled state"""
        if self._icon:
            self._icon.icon = self.create_icon_image(enabled)
    
    def run(self) -> None:
        """Start the tray icon (blocking)"""
        self._icon = Icon(
            'ReHebrew',
            self.create_icon_image(True),
            'ReHebrew - Hebrew Text Converter',
            self._create_menu()
        )
        self._icon.run()
    
    def stop(self) -> None:
        """Stop the tray icon"""
        if self._icon:
            self._icon.stop()
    
    @property
    def logo_image(self) -> Optional[Image.Image]:
        """Get the loaded logo image"""
        return self._logo_image

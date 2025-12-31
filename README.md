# ReHebrew 🇮🇱

**Convert English-layout gibberish to Hebrew text with a single keystroke!**

## The Problem

When typing in Hebrew, users often forget to switch their keyboard layout from English to Hebrew. The result is gibberish like `akunh` instead of `שלומי`. ReHebrew fixes this instantly!

## Features

✅ **System Tray Application** - Runs silently in the background  
✅ **Global Hotkey** - Press `Ctrl+Shift+H` to convert selected text  
✅ **Smart Conversion** - Maps English keys to Hebrew keyboard layout  
✅ **Lightweight** - Minimal CPU and memory usage  
✅ **Auto-Start** - Optional Windows startup  
✅ **Notifications** - Subtle feedback when needed  

## Installation

### Prerequisites
- Python 3.8 or higher
- Windows 10/11

### Setup

1. **Clone or download** this repository

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python rehebrew.py
   ```

## Usage

1. **Start ReHebrew** - The app will appear in your system tray
2. **Type text** (forgetting to switch to Hebrew layout)
3. **Select the gibberish text**
4. **Press `Ctrl+Shift+H`** - Text is instantly converted to Hebrew!

### Example

| Before | After |
|--------|-------|
| `akunh` | `שלומי` |
| `,usu` | `טוב` |
| `cuerv` | `בוקר` |

## System Tray Menu

Right-click the tray icon for options:

- **Enable ReHebrew** - Toggle conversion on/off
- **Start with Windows** - Enable auto-start
- **About** - Version info
- **Exit** - Close the application

## Configuration

Settings are stored in `config.json`:

```json
{
  "shortcut": "ctrl+shift+h",
  "auto_start": false,
  "enabled": true,
  "show_notifications": true
}
```

### Customizing the Shortcut

Edit `config.json` and change the `shortcut` value. Examples:
- `"ctrl+shift+h"` (default)
- `"ctrl+alt+h"`
- `"win+h"`

## Keyboard Mapping

ReHebrew uses the standard Israeli Hebrew keyboard layout:

| English | Hebrew | English | Hebrew |
|---------|--------|---------|--------|
| q | / | a | ש |
| w | ' | s | ד |
| e | ק | d | ג |
| r | ר | f | כ |
| t | א | g | ע |
| y | ט | h | י |
| u | ו | j | ח |
| i | ן | k | ל |
| o | ם | l | ך |
| p | פ | z | ז |
| | | x | ס |
| | | c | ב |
| | | v | ה |
| | | b | נ |
| | | n | מ |
| | | m | צ |

## Building Executable (Optional)

To create a standalone `.exe` file:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico --name=ReHebrew rehebrew.py
```

The executable will be in the `dist` folder.

## Troubleshooting

### Hotkey not working?
- Make sure no other application is using the same hotkey
- Try running as Administrator
- Check that ReHebrew is enabled (tray icon should be blue)

### Text not converting?
- Ensure text is selected before pressing the hotkey
- The clipboard must be accessible

### App not starting?
- Check if another instance is already running
- Verify all dependencies are installed

## Security & Privacy

🔒 **100% Local Processing** - No data is ever sent externally  
🔒 **No Keylogging** - Only responds to the specific hotkey  
🔒 **Open Source** - Full transparency of the code  

## Future Plans

- [ ] Auto-detect gibberish and suggest conversion
- [ ] Support for Arabic and other RTL languages
- [ ] macOS and Linux versions
- [ ] Settings GUI window
- [ ] Reverse conversion (Hebrew to English layout)

## License

MIT License - Feel free to use, modify, and distribute!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Made with ❤️ for Hebrew speakers everywhere
